# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import hashlib
import io
import secrets
import string
from calendar import month_name

import qrcode
from stdnum.es import vat as es_vat

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools.pdf import DEFAULT_PDF_DATETIME_FORMAT, PdfFileReader, PdfFileWriter

# Resolución de 5/06/2026 (BOE-A-2026-12784), ap. Segundo.1: the PDF must
# stay under this size (native-digital, no scans), or the QR-driven public
# download could be rejected downstream.
MAX_PDF_SIZE_BYTES = 5 * 1024 * 1024

# Alphanumeric only (no '-'/'_' like secrets.token_urlsafe): the token is
# printed on the PDF and may have to be read or typed by hand, and plain
# alnum text has no natural break points for a text renderer/PDF viewer to
# split on mid-token. 22 chars from a 62-symbol alphabet is ~131 bits of
# entropy, at least as strong as token_urlsafe(16)'s 128 bits.
TOKEN_ALPHABET = string.ascii_letters + string.digits
TOKEN_LENGTH = 22

# Modifiable fields whose in-route change must go through the Método A
# wizard (ap. Quinto) instead of a direct write(), together with the label
# to print in the change history table of the report.
MODIFIABLE_FIELDS = {
    "cmr_tractor_id": lambda self: _("Tractor"),
    "cmr_tractor_license_plate": lambda self: _("Tractor Plate"),
    "cmr_semi_trailer_id": lambda self: _("Trailer"),
    "cmr_semi_trailer_license_plate": lambda self: _("Trailer Plate"),
    "cmr_transportation_id": lambda self: _("Carrier"),
    "cmr_special_traffic_authorization": lambda self: _(
        "Special Circulation Authorization"
    ),
    "cmr_observations": lambda self: _("Observations"),
}


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    cmr_way_out_id = fields.Many2one(
        string="Way out", comodel_name="res.city", copy=False
    )
    cmr_destination_id = fields.Many2one(
        string="Destination", comodel_name="res.city", copy=False
    )
    cmr_loader_id = fields.Many2one(
        string="loader", comodel_name="res.partner", copy=False
    )
    cmr_loader_vat = fields.Char(string="Loader VAT", copy=False)
    cmr_loader_address = fields.Text(string="Loader Address")
    cmr_transportation_id = fields.Many2one(
        string="Transportations", comodel_name="res.partner", copy=False
    )
    cmr_transportation_vat = fields.Char(string="Transportation VAT", copy=False)
    cmr_tractor_license_plate = fields.Char(string="Tractor license plate", copy=False)
    cmr_semi_trailer_license_plate = fields.Char(
        string="Semi-trailer license plate", copy=False
    )
    cmr_driver_id = fields.Many2one(
        string="Driver", comodel_name="res.partner", copy=False
    )
    site_date_info = fields.Char(
        string="Site and date info", compute="_compute_site_date_info"
    )
    cmr_second_driver_id = fields.Many2one(
        string="Second Driver", comodel_name="res.partner", copy=False
    )
    cmr_tractor_id = fields.Many2one(
        string="Tractor",
        comodel_name="fleet.vehicle",
        copy=False,
    )
    cmr_semi_trailer_id = fields.Many2one(
        string="Semi-Trailer",
        comodel_name="fleet.vehicle",
        copy=False,
    )
    cmr_special_traffic_authorization = fields.Boolean(
        string="Special Traffic Authorization",
        default=False,
        copy=False,
    )
    deca_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("issued", "Issued"),
            ("modified", "Modified"),
            ("closed", "Closed"),
            ("superseded", "Superseded"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        copy=False,
        required=True,
    )
    token = fields.Char(
        copy=False,
        readonly=True,
        help="Unguessable identifier used to build the public download URL. "
        "Generated once, on issue (see _generate_token), enforced unique "
        "at the database level (token_unique): it is the "
        "only access control on the public PDF, so it must never be "
        "sequential or derived from record data.",
    )
    issued_on = fields.Datetime(copy=False, readonly=True)
    last_modified_on = fields.Datetime(copy=False, readonly=True)
    pdf_sha256 = fields.Char(
        string="PDF SHA-256",
        copy=False,
        readonly=True,
        help="SHA-256 of the PDF attachment's exact bytes, recomputed every "
        "time the PDF is (re)generated. Verify Integrity recomputes the "
        "hash of the attachment as stored right now and compares it "
        "against this value, to prove the file an inspector would open "
        "hasn't been swapped or corrupted since it was last issued or "
        "modified.",
    )
    public_url = fields.Char(compute="_compute_public_url")
    qr_attachment_id = fields.Many2one("ir.attachment", copy=False, readonly=True)
    special_auth = fields.Char(string="Special Circulation Authorization")
    transport_date = fields.Date(compute="_compute_transport_date", store=True)
    cmr_observations = fields.Text(
        string="Observations",
    )
    pdf_attachment_id = fields.Many2one("ir.attachment", copy=False, readonly=True)
    supersedes_id = fields.Many2one(
        comodel_name="stock.picking.batch",
        string="Supersedes",
        readonly=True,
        copy=False,
        help="The previous DeCA this one replaced (Método B, ap. Quinto.2): "
        "set only when this record was created by reissuing an earlier one "
        "under a brand-new token/URL/QR, as opposed to a fresh DeCA for a "
        "delivery that never had one.",
    )
    deca_access_log_ids = fields.One2many(
        string="Deca Access Logs",
        comodel_name="stock.picking.batch.deca.access.log",
        inverse_name="picking_batch_id",
        readonly=True,
        copy=False,
    )
    deca_change_ids = fields.One2many(
        comodel_name="stock.picking.batch.deca.change",
        inverse_name="batch_id",
        string="Change History",
        readonly=True,
        copy=False,
    )
    deca_can_cancel = fields.Boolean(
        compute="_compute_can_cancel",
        help="Whether cancelling is even on the table right now: issued or "
        "modified, and the transport hasn't started yet. Not a Resolución "
        "requirement (unlike Método A/B) -- once a service may already be "
        "underway, calling it off isn't a thing the same way; that's what "
        "Método A/B are for instead.",
    )

    _sql_constraints = [
        (
            "token_unique",
            "unique(token)",
            "This DeCA token collided with an existing one -- issue the DeCA again.",
        ),
    ]

    @api.depends("token")
    def _compute_public_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for batch in self:
            batch.public_url = (
                "%s/deca/%s" % (base_url, batch.token) if batch.token else False
            )

    @api.depends("picking_ids.scheduled_date")
    def _compute_transport_date(self):
        for batch in self:
            dates = batch.picking_ids.mapped("scheduled_date")
            batch.transport_date = max(dates) if dates else False

    @api.depends("deca_state", "picking_ids.scheduled_date")
    def _compute_can_cancel(self):
        today = fields.Date.context_today(self)
        for batch in self:
            dates = batch.picking_ids.mapped("scheduled_date")
            earliest = min(dates) if dates else False
            # The earliest grouped delivery's date, not the latest
            # (transport_date below): the whole DeCA stops being
            # cancellable the moment even ONE of its deliveries may
            # already be under way -- there's no partial cancellation.
            batch.deca_can_cancel = (
                batch.state in ("issued", "modified")
                and bool(earliest)
                and earliest > today
            )

    @api.depends("cmr_way_out_id")
    def _compute_site_date_info(self):
        my_date = fields.Date.context_today(self)
        for picking in self:
            city = picking.cmr_way_out_id.name if picking.cmr_way_out_id else ""
            month = _(month_name[my_date.month])
            picking.site_date_info = (
                f"{city}, {my_date.day} of {month} of {my_date.year}"
            )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        parent_onchange = getattr(super(), "onchange_partner_id", None)
        res = {}
        if parent_onchange:
            res = parent_onchange()
        if self.partner_id:
            self.cmr_driver_id = self.partner_id.driver_id.id
            self.cmr_tractor_id = self.partner_id.tractor_id.id
            self.cmr_semi_trailer_id = self.partner_id.semi_trailer_id.id
        return res

    @api.onchange("cmr_loader_id")
    def onchange_cmr_loader_id(self):
        self.cmr_loader_vat = self.cmr_loader_id.vat or ""
        self.cmr_loader_address = self.cmr_loader_id.contact_address or ""

    @api.onchange("cmr_transportation_id")
    def onchange_cmr_transportation_id(self):
        self.cmr_transportation_vat = self.cmr_transportation_id.vat or ""

    @api.onchange("cmr_tractor_id")
    def _onchange_cmr_tractor_id(self):
        for picking in self:
            if picking.cmr_tractor_id:
                picking.cmr_tractor_license_plate = picking.cmr_tractor_id.license_plate
                picking.cmr_driver_id = picking.cmr_tractor_id.driver_id.id

    @api.onchange("cmr_semi_trailer_id")
    def _onchange_cmr_semi_trailer_id(self):
        for picking in self:
            if picking.cmr_semi_trailer_id:
                picking.cmr_semi_trailer_license_plate = (
                    picking.cmr_semi_trailer_id.license_plate
                )

    @api.onchange("cmr_tractor_id", "cmr_semi_trailer_id")
    def _onchange_cmr_tractor_semi_trailer(self):
        for picking in self:
            picking.cmr_special_traffic_authorization = any(
                (
                    picking.cmr_tractor_id.special_traffic_authorization,
                    picking.cmr_semi_trailer_id.special_traffic_authorization,
                )
            )

    @api.onchange("cmr_driver_id")
    def _onchange_cmr_driver_id(self):
        for picking in self:
            if picking.cmr_driver_id:
                picking.cmr_loader_id = picking.cmr_driver_id.parent_id.id

    def action_issue_deca(self):
        self.ensure_one()
        if self.deca_state != "draft":
            raise UserError(_("Only a draft DeCA can be issued."))
        pickings = self.picking_ids.filtered(lambda z: z.state != "done")
        if pickings:
            raise UserError(
                _("To generate DeCA, all pickings must be in the 'Done' state.")
            )
        missing = [
            label
            for field_name, label in (
                ("cmr_loader_id", _("Shipper")),
                ("cmr_loader_vat", _("Shipper VAT")),
                ("cmr_transportation_id", _("Carrier")),
                ("cmr_transportation_vat", _("Carrier VAT")),
                ("cmr_tractor_license_plate", _("Tractor Plate")),
            )
            if not self[field_name]
        ]
        if not self.move_ids:
            missing.append(_("move_ids"))

        # Only checked when present, so a genuinely missing VAT is reported
        # once (as "missing"), not twice.
        invalid_vat = [
            label
            for field_name, label in (
                ("cmr_loader_vat", _("Shipper VAT")),
                ("cmr_transportation_vat", _("Carrier VAT")),
            )
            if self[field_name] and not self._is_valid_spanish_vat(self[field_name])
        ]

        # Ap. Sexto.1: every grouped delivery must share the same shipper
        # and carrier as each other -- the onchange warning is easy to
        # miss or simply never reached by a non-UI caller, so it's
        # re-checked hard here too, same as VAT above. Only meaningful
        # once there's more than one delivery -- see the matching comment
        # in _onchange_picking_ids for why a lone delivery is never
        # checked, and _group_mismatch_lines for why this compares the
        # deliveries against EACH OTHER rather than against this DeCA's
        # own shipper_partner_id/carrier_partner_id.
        errors = []
        if missing:
            errors.append(
                _(
                    "Complete these fields before issuing the DeCA: %(fields)s",
                    fields=", ".join(missing),
                )
            )
        if invalid_vat:
            errors.append(
                _(
                    "These are not valid Spanish NIF/NIE/CIF numbers: %(fields)s",
                    fields=", ".join(invalid_vat),
                )
            )
        if errors:
            raise UserError("\n".join(errors))

        now = fields.Datetime.now()
        vals = {
            "token": self.token or self._generate_token(),
            "issued_on": now,
            "last_modified_on": now,
            "deca_state": "issued",
        }
        self.with_context(deca_internal_write=True).write(vals)
        self._generate_qr_attachment()
        self._regenerate_pdf()
        self.message_post(
            body=_(
                "DeCA issued. SHA-256: %(hash)s. Public URL: %(url)s",
                hash=self.pdf_sha256,
                url=self.public_url,
            )
        )
        # Método B (ap. Quinto.2): the original only actually stops serving
        # its PDF once THIS replacement has a real public URL to send
        # visitors to -- flipping it the moment the draft was created (in
        # _reissue) would leave a window where neither document is
        # downloadable, which is worse than just keeping the original live
        # a little longer.
        if self.supersedes_id and self.supersedes_id.state in ("issued", "modified"):
            original = self.supersedes_id
            original.with_context(deca_internal_write=True).write(
                {"state": "superseded", "superseded_by_id": self.id}
            )
            original.message_post(
                body=_(
                    "Superseded by %(new)s (Método B). Reason: %(reason)s. "
                    "The original PDF and token are preserved for "
                    "traceability but no longer served publicly.",
                    new=self.name,
                    reason=self.reissue_reason,
                )
            )
        return True

    @api.model
    def _is_valid_spanish_vat(self, vat_number):
        """NIF (individuals), NIE (foreigners) and CIF (companies) each have
        their own check-digit algorithm -- stdnum.es.vat (already vendored
        by Odoo itself, used internally by base_vat) covers all three and
        already normalizes formatting on its own: 'ES-B12345678',
        'ES B12345678', 'B-12345678' and 'b12345678' all check out
        identically. Deliberately not used to rewrite the stored value,
        only to validate it as typed -- shipper_vat/carrier_vat are a
        snapshot of the partner's record at issue time, not something this
        module should silently reformat.
        """
        return bool(vat_number) and es_vat.is_valid(vat_number)

    @api.model
    def _generate_token(self):
        # At ~131 bits of entropy an actual collision is astronomically
        # unlikely -- this loop is belt-and-suspenders over the real
        # guarantee, the token_unique SQL constraint, so a collision (of
        # this or a future, weaker generator) fails here with a fresh
        # candidate instead of a raw IntegrityError out of write().
        while True:
            token = "".join(secrets.choice(TOKEN_ALPHABET) for _ in range(TOKEN_LENGTH))
            if not self.sudo().search_count([("token", "=", token)]):
                return token

    def _generate_qr_attachment(self):
        self.ensure_one()
        qr_image = qrcode.make(self.public_url)
        buffer = io.BytesIO()
        qr_image.save(buffer, format="PNG")
        attachment = self.env["ir.attachment"].create(
            {
                "name": "%s_qr.png" % self.name,
                "datas": base64.b64encode(buffer.getvalue()),
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "image/png",
            }
        )
        self.with_context(deca_internal_write=True).write(
            {"qr_attachment_id": attachment.id}
        )

    def _regenerate_pdf(self):
        """(Re)render the DeCA report and overwrite the existing PDF
        attachment's content in place: same attachment id -> same public
        URL/token/QR, which is the whole point of Método A (Resolución,
        ap. Quinto) -- a modification must never force the driver to scan a
        new QR.
        """
        self.ensure_one()
        pdf_content, report_type = self.env["ir.actions.report"]._render_qweb_pdf(
            "stock_picking_batch_cmr_deca.action_report_deca", res_ids=self.ids
        )
        if report_type != "pdf":
            # Odoo's own --test-enable short-circuit (ir_actions_report.py,
            # _pre_render_qweb_pdf): falls back to an HTML render so the
            # test suite doesn't shell out to wkhtmltopdf on every report
            # call. A test that needs a real PDF opts in itself with
            # with_context(force_report_rendering=True), same as Odoo
            # core's own report tests do -- this method must not force it
            # unconditionally, or every test anywhere that touches a DeCA
            # would always pay for a real wkhtmltopdf render.
            raise UserError(_("Could not render the DeCA as a PDF document."))
        pdf_content = self._stamp_pdf_dates(pdf_content)
        if len(pdf_content) > MAX_PDF_SIZE_BYTES:
            raise UserError(
                _(
                    "The generated DeCA PDF exceeds the 5 MB limit set by the Resolución."
                )
            )
        attachment_vals = {
            "name": "%s.pdf" % self.name,
            "datas": base64.b64encode(pdf_content),
            "res_model": self._name,
            "res_id": self.id,
            "mimetype": "application/pdf",
        }
        pdf_sha256 = hashlib.sha256(pdf_content).hexdigest()
        if self.pdf_attachment_id:
            self.pdf_attachment_id.with_context(deca_internal_write=True).write(
                attachment_vals
            )
            self.with_context(deca_internal_write=True).write(
                {"pdf_sha256": pdf_sha256}
            )
        else:
            attachment = self.env["ir.attachment"].create(attachment_vals)
            self.with_context(deca_internal_write=True).write(
                {"pdf_attachment_id": attachment.id, "pdf_sha256": pdf_sha256}
            )

    def _stamp_pdf_dates(self, pdf_content):
        """Write /CreationDate (first issue) and /ModDate (now) as real PDF
        metadata, not just Odoo columns -- required explicitly by the
        Resolución, ap. Segundo.1. Reuses odoo.tools.pdf (already vendored
        by Odoo for its own PDF/A and Factur-X handling) instead of adding
        a new PyPDF2/pypdf dependency of our own.
        """
        self.ensure_one()
        creation_dt = fields.Datetime.from_string(
            self.issued_on or fields.Datetime.now()
        )
        mod_dt = fields.Datetime.now()
        reader = PdfFileReader(io.BytesIO(pdf_content), strict=False)
        writer = PdfFileWriter()
        for page in range(reader.getNumPages()):
            writer.addPage(reader.getPage(page))
        add_metadata = getattr(writer, "add_metadata", None) or writer.addMetadata
        add_metadata(
            {
                "/CreationDate": creation_dt.strftime(DEFAULT_PDF_DATETIME_FORMAT),
                "/ModDate": mod_dt.strftime(DEFAULT_PDF_DATETIME_FORMAT),
            }
        )
        buffer = io.BytesIO()
        writer.write(buffer)
        return buffer.getvalue()

    def action_view_pdf(self):
        """Open the exact stored PDF attachment in a new tab -- the same
        bytes the public URL would serve, but reachable from the backend
        without leaving Odoo or knowing the token. Works on a superseded
        DeCA too: its PDF is preserved (ap. Quinto.2) even though its
        public URL no longer serves it directly.
        """
        self.ensure_one()
        if not self.pdf_attachment_id:
            raise UserError(_("This DeCA has no PDF yet."))
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=false" % self.pdf_attachment_id.id,
            "target": "new",
        }

    # -------------------------------------------------------------------
    # Immutability (ap. 3.10 / §2.4): an issued DeCA can only change through
    # _apply_change above, never through a direct write() or unlink().
    # -------------------------------------------------------------------

    def write(self, vals):
        if "change_deca" in self.env.context and self.env.context.get(
            "change_deca", False
        ):
            for batch in self:
                batch.picking_ids.write(vals)
        if "qr_attachment_id" in vals and vals.get("qr_attachment_id", False):
            self._put_cmr_info_in_pickings()
        if self.env.context.get("deca_internal_write") or (
            len(vals) == 1 and "message_main_attachment_id" in vals
        ):
            return super().write(vals)
        for batch in self:
            if batch.deca_state != "draft":
                raise UserError(
                    _(
                        "%(name)s is issued and immutable: register a "
                        "modification instead of editing it directly.",
                        name=batch.name,
                    )
                )
        old_picking_ids = (
            {batch.id: batch.picking_ids for batch in self}
            if "picking_ids" in vals
            else {}
        )
        if "picking_ids" in vals:
            for batch in self:
                old_picking_ids = batch.picking_ids
                newly_added = self.env["stock.picking"]
                for command in vals["picking_ids"]:
                    if command[0] == 4:
                        # (4, picking_id, 0) -> añadir un picking
                        picking = self.env["stock.picking"].browse(command[1])

                        if picking not in old_picking_ids:
                            newly_added |= picking
                    elif command[0] == 6:
                        # (6, 0, [ids]) -> reemplazar todos los pickings
                        new_ids = set(command[2])
                        old_ids = set(old_picking_ids.ids)

                        added_ids = new_ids - old_ids

                        if added_ids:
                            newly_added |= self.env["stock.picking"].browse(
                                list(added_ids)
                            )
                if newly_added:
                    batch._log_picking_coverage(
                        newly_added,
                        generated=False,
                    )
        return super().write(vals)

    def unlink(self):
        for batch in self:
            if batch.deca_state != "draft":
                raise UserError(
                    _("%(name)s is issued and cannot be deleted.", name=batch.name)
                )
        return super().unlink()

    def _put_cmr_info_in_pickings(self):
        for batch in self:
            vals = batch._get_cmr_info()
            batch.picking_ids.write(vals)

    def _get_cmr_info(self):
        vals = {
            "cmr_loader_id": self.cmr_loader_id.id if self.cmr_loader_id else False,
            "cmr_loader_vat": self.cmr_loader_vat,
            "cmr_loader_address": self.cmr_loader_address,
            "cmr_transportation_id": (
                self.cmr_transportation_id.id if self.cmr_transportation_id else False
            ),
            "cmr_transportation_vat": self.cmr_transportation_vat,
            "cmr_driver_id": self.cmr_driver_id.id if self.cmr_driver_id else False,
            "cmr_second_driver_id": (
                self.cmr_second_driver_id.id if self.cmr_second_driver_id else False
            ),
            "cmr_tractor_id": self.cmr_tractor_id.id if self.cmr_tractor_id else False,
            "cmr_tractor_license_plate": self.cmr_tractor_license_plate,
            "cmr_semi_trailer_id": (
                self.cmr_semi_trailer_id.id if self.cmr_semi_trailer_id else False
            ),
            "cmr_semi_trailer_license_plate": self.cmr_semi_trailer_license_plate,
            "cmr_special_traffic_authorization": self.cmr_special_traffic_authorization,
            "cmr_observations": self.cmr_observations,
        }
        return vals

    def _log_picking_coverage(self, pickings, generated):
        """Posts on each of pickings' OWN chatter that it's now covered by
        this DeCA -- both create() (a brand-new DeCA) and write() (adding
        to picking_ids on an existing draft, e.g. via the form's own
        selector) route through this, so neither path leaves the picking
        silent about something that directly concerns it.
        """
        for picking in pickings:
            others = self.picking_ids - picking
            if generated:
                body = (
                    _(
                        "DeCA %(name)s generated, grouping this delivery "
                        "together with: %(others)s (ap. Sexto.1).",
                        name=self.name,
                        others=", ".join(others.mapped("display_name")),
                    )
                    if others
                    else _("DeCA %(name)s generated for this delivery.", name=self.name)
                )
            else:
                body = (
                    _(
                        "Added to DeCA %(name)s, grouped together with: "
                        "%(others)s (ap. Sexto.1).",
                        name=self.name,
                        others=", ".join(others.mapped("display_name")),
                    )
                    if others
                    else _("Added to DeCA %(name)s.", name=self.name)
                )
            picking.message_post(body=body)

    def _log_access(self, ip_address, method, status_code):
        """Called by the public controller (/deca/<token>) on every request
        that matches a real DeCA, whether or not it actually serves the
        PDF (a 404 on a token that exists but is closed is itself
        evidence -- someone tried after the retention window shut it).
        Deliberately takes the request details as plain arguments instead
        of reaching into odoo.http.request itself, so this stays callable
        (and testable) outside of an actual HTTP request. Does NOT commit
        itself -- the 404 path in the controller must do that explicitly
        (see its comment), but a plain model-level caller (tests, future
        code) must stay free to roll this back like any other write.
        """
        self.ensure_one()
        self.env["stock.picking.batch.deca.access.log"].sudo().create(
            {
                "picking_batch_id": self.id,
                "ip_address": ip_address,
                "method": method,
                "status_code": status_code,
            }
        )

    def action_open_modify_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Register DeCA Modification"),
            "res_model": "wiz.deca.modify",
            "view_mode": "form",
            "target": "new",
            "context": {**self.env.context, "default_batch_id": self.id},
        }

    def _apply_change(self, field_name, new_value, reason):
        self.ensure_one()
        vehicle_obj = self.env["fleet.vehicle"]
        if self.deca_state not in ("issued", "modified"):
            raise UserError(_("Only an issued DeCA can be modified."))
        if field_name not in MODIFIABLE_FIELDS:
            raise UserError(_("This field cannot be modified this way."))

        field = self._fields[field_name]
        old_value = field.convert_to_export(self[field_name], self) or ""
        if field.type == "many2one":
            new_record = self.env[field.comodel_name].browse(int(new_value))
            new_display_value = new_record.display_name
            write_value = new_record.id
            unchanged = self[field_name].id == write_value
        else:
            new_display_value = new_value
            write_value = new_value
            unchanged = (self[field_name] or "") == (new_value or "")
        if unchanged:
            raise UserError(
                _(
                    "The new value is the same as the current one; there is "
                    "nothing to register."
                )
            )

        self.with_context(deca_internal_write=True, change_deca=True).write(
            {field_name: write_value}
        )

        if field_name == "cmr_tractor_id":
            vehicle = vehicle_obj.browse(write_value)
            self.with_context(deca_internal_write=True, change_deca=True).write(
                {"cmr_tractor_license_plate": vehicle.license_plate}
            )
        if field_name == "cmr_semi_trailer_id":
            vehicle = vehicle_obj.browse(write_value)
            self.with_context(deca_internal_write=True, change_deca=True).write(
                {"cmr_semi_trailer_license_plate": vehicle.license_plate}
            )
        self.env["stock.picking.batch.deca.change"].create(
            {
                "batch_id": self.id,
                "field_label": MODIFIABLE_FIELDS[field_name](self),
                "old_value": old_value,
                "new_value": new_display_value,
                "reason": reason,
            }
        )
        self.with_context(deca_internal_write=True).write(
            {"deca_state": "modified", "last_modified_on": fields.Datetime.now()}
        )
        self._regenerate_pdf()
        self.message_post(
            body=_(
                "%(field)s changed: %(old)s → %(new)s. Reason: %(reason)s. "
                "SHA-256: %(hash)s. Public URL: %(url)s",
                field=MODIFIABLE_FIELDS[field_name](self),
                old=old_value or _("(empty)"),
                new=new_display_value,
                reason=reason,
                hash=self.pdf_sha256,
                url=self.public_url,
            )
        )

    def action_open_reissue_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Reissue DeCA"),
            "res_model": "wiz.deca.reissue",
            "view_mode": "form",
            "target": "new",
            "context": {**self.env.context, "default_batch_id": self.id},
        }

    def _reissue(self, reason):
        """Ap. Quinto.2: "Generación de un nuevo fichero electrónico [...]
        tendrá una nueva URL [...] se deberá conservar el fichero original
        a los efectos de trazabilidad". Returns the new (draft) DeCA so the
        caller can open it for review -- this only creates the successor,
        it does not touch the original at all yet. The original keeps
        serving its PDF exactly as before until this replacement is
        actually issued (see action_issue): flipping it the moment a draft
        exists would leave a window where neither document has a working
        public URL.
        """
        self.ensure_one()
        if self.state not in ("issued", "modified"):
            raise UserError(_("Only an issued DeCA can be reissued."))
        new_deca = self.copy(
            {
                "picking_ids": [fields.Command.set(self.picking_ids.ids)],
                "supersedes_id": self.id,
                "reissue_reason": reason,
            }
        )
        # draft_replacement_id has no real field dependency to trigger on
        # here -- it's a search on ANOTHER record's supersedes_id/state,
        # which this record's own @api.depends("state") can't express
        # (self.state doesn't change by creating a reissue). Without this,
        # the original would keep showing its stale (empty) cached value
        # for the rest of the transaction.
        self.invalidate_recordset(["draft_replacement_id"])
        # Force a clean sync to the picking's current operations rather than
        # trust whatever copy() did with a compute(store=True) field -- the
        # new draft must start in the same "always in sync while draft"
        # state as any other freshly created DeCA (see _compute_line_ids).
        new_deca._compute_line_ids()
        self.message_post(
            body=_(
                "Reissue started (Método B): %(new)s will replace this "
                "document once issued. Reason: %(reason)s",
                new=new_deca.name,
                reason=reason,
            )
        )
        new_deca.message_post(
            body=_(
                "Reissued from %(old)s (Método B). Reason: %(reason)s",
                old=self.name,
                reason=reason,
            )
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("DeCA"),
            "res_model": "l10n.es.deca",
            "view_mode": "form",
            "res_id": new_deca.id,
        }

    def action_open_cancel_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Cancel DeCA"),
            "res_model": "wiz.deca.cancel",
            "view_mode": "form",
            "target": "new",
            "context": {**self.env.context, "default_batch_id": self.id},
        }

    def _deca_cancel(self, reason):
        self.ensure_one()
        if not self.env.user.has_group(
            "stock_picking_batch_cmr_deca.group_deca_manager"
        ):
            raise AccessError(_("Only a DeCA Manager can cancel a DeCA."))
        if not self.deca_can_cancel:
            if self.state not in ("issued", "modified"):
                raise UserError(_("Only an issued DeCA can be cancelled."))
            raise UserError(
                _("This DeCA cannot be cancelled once its transport date has arrived.")
            )
        self.with_context(deca_internal_write=True).write({"deca_state": "cancelled"})
        self.message_post(
            body=_(
                "Cancelled before the service started. Reason: %(reason)s",
                reason=reason,
            )
        )

    def action_deca_send_email(self):
        self.ensure_one()
        template = self.env.ref("stock_picking_batch_cmr_deca.mail_template_deca")
        partner_ids = (self.cmr_loader_id | self.cmr_transportation_id).ids
        return {
            "type": "ir.actions.act_window",
            "name": _("Send DeCA"),
            "res_model": "mail.compose.message",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_model": self._name,
                "default_res_ids": self.ids,
                "default_template_id": template.id,
                "default_partner_ids": partner_ids,
                "default_composition_mode": "comment",
            },
        }

    def action_deca_verify_integrity(self):
        """Recompute the SHA-256 of the PDF attachment exactly as stored
        right now and compare it against pdf_sha256 (set at the last
        issue/modification, in _regenerate_pdf). A mismatch means the
        attachment's bytes changed through some path other than this
        module's own report generation -- direct DB tampering, a restore
        from an inconsistent backup, etc.
        """
        self.ensure_one()
        if not self.pdf_attachment_id or not self.pdf_sha256:
            raise UserError(_("There is no issued PDF to verify yet."))
        current_hash = hashlib.sha256(
            base64.b64decode(self.pdf_attachment_id.datas)
        ).hexdigest()
        if current_hash != self.pdf_sha256:
            self.message_post(
                body=_(
                    "Integrity check FAILED: the stored PDF no longer matches "
                    "its recorded SHA-256. Recorded: %(expected)s. Current: "
                    "%(actual)s.",
                    expected=self.pdf_sha256,
                    actual=current_hash,
                )
            )
            raise UserError(
                _(
                    "Integrity check failed: the PDF attachment does not "
                    "match its recorded SHA-256. See the chatter for details."
                )
            )
        self.message_post(
            body=_(
                "Integrity verified: the stored PDF matches its recorded "
                "SHA-256 (%(hash)s).",
                hash=self.pdf_sha256,
            )
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Integrity verified"),
                "message": _("The PDF matches its recorded SHA-256 hash."),
                "type": "success",
                "sticky": False,
            },
        }
