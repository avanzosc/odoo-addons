# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    tractor_license_plate_id = fields.Many2one(
        string="Main vehicle or tractor licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
    )
    trailer_license_plate_id = fields.Many2one(
        string="Trailer or semi-trailer licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
    )
    deca_notes = fields.Text(string="DECA Notes")

    # Vehicle field -> DeCA char field of l10n_es_deca_oca whose changes are
    # kept in the history printed (struck through) on the DeCA.
    _DECA_VEHICLE_PLATE_FIELDS = {
        "tractor_license_plate_id": "tractor_license_plate",
        "trailer_license_plate_id": "trailer_license_plate",
    }

    def _get_deca_plate(self, plate_field, vehicle):
        """Plate of ``vehicle`` as stored in the DeCA char field: cut to the
        field size like the ORM does, so comparing it with the stored value
        does not add the same plate to the history again."""
        plate = vehicle.license_plate or ""
        size = self._fields[plate_field].size
        return plate[:size] if size else plate

    def _prepare_deca_plate_vals(self, vals):
        """Add to ``vals`` the plate of the vehicles being written, so the base
        ``write`` stores the previous plate in the DeCA history."""
        vals = dict(vals)
        for vehicle_field, plate_field in self._DECA_VEHICLE_PLATE_FIELDS.items():
            if vehicle_field in vals and plate_field not in vals:
                vehicle = self.env["fleet.vehicle"].browse(vals[vehicle_field])
                vals[plate_field] = self._get_deca_plate(plate_field, vehicle)
        return vals

    def _sync_deca_plates(self):
        """Copy the current vehicle plates to the DeCA char fields, only when
        they differ (e.g. the plate was changed on the vehicle itself)."""
        for picking in self:
            vals = {}
            for vehicle_field, plate_field in self._DECA_VEHICLE_PLATE_FIELDS.items():
                plate = picking._get_deca_plate(plate_field, picking[vehicle_field])
                if (picking[plate_field] or "") != plate:
                    vals[plate_field] = plate
            if vals:
                picking.write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._prepare_deca_plate_vals(vals) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        return super().write(self._prepare_deca_plate_vals(vals))

    def _check_deca_required_fields(self):
        for picking in self:
            missing = []
            if not picking.tractor_license_plate_id:
                missing.append(
                    self.env._(
                        "You must define the Main vehicle or tractor licence plate."
                    )
                )
            picking._sync_deca_plates()
            if not picking.carrier_contact_id:
                missing.append(self.env._("You must define the Carrier contact."))
            elif not picking.carrier_contact_id.vat:
                missing.append(self.env._("Carrier NIF (VAT)"))
            for move in picking.move_ids_without_package.filtered(
                lambda x: x.product_id
            ):
                product_data = {
                    "product_name": move.product_id.name,
                    "quantity": move.product_uom_qty,
                    "deca_weight": move.deca_weight,
                }
                if not move.place_of_loading_id:
                    missing.append(
                        self.env._(
                            "You must define the Place of loading"
                            " for product: %(product_name)s, quantity: "
                            "%(quantity)s, DECA Weight: %(deca_weight)s"
                        )
                        % product_data
                    )
                elif not move.place_of_loading_id.vat:
                    missing.append(
                        self.env._(
                            "You must define the VAT for Sender / Place"
                            " of loading: %(sender_name)s for product: "
                            "%(product_name)s, quantity: %(quantity)s,"
                            " DECA Weight: %(deca_weight)s"
                        )
                        % {
                            **product_data,
                            "sender_name": move.place_of_loading_id.name,
                        }
                    )
                if not move.place_of_delivery_ids:
                    missing.append(
                        self.env._(
                            "You must define the Place of delivery"
                            " for product: %(product_name)s, quantity:"
                            " %(quantity)s, DECA Weight: %(deca_weight)s"
                        )
                        % product_data
                    )
                else:
                    for delivery in move.place_of_delivery_ids:
                        if not delivery.vat:
                            missing.append(
                                self.env._(
                                    "You must define the VAT for Consignee / Place"
                                    " of delivery: %(consignee_name)s for product:"
                                    " %(product_name)s, quantity: %(quantity)s,"
                                    " DECA Weight: %(deca_weight)s"
                                )
                                % {
                                    "consignee_name": delivery.name,
                                }
                            )
            if missing:
                raise UserError(
                    self.env._(
                        "The following data is missing for the DeCA "
                        "report for picking %(picking)s:\n%(missing)s",
                        picking=picking.name,
                        missing="\n".join(f"- {m}" for m in missing),
                    )
                )
        return super()._check_deca_required_fields()

    def _get_deca_report_data(self):
        self.ensure_one()
        if self.state != "done":
            raise UserError(
                self.env._(
                    "To generate the DECA report, the picking status must be 'Done'."
                )
            )
        values = super()._get_deca_report_data()
        contractual = {
            name: self.partner_id[name] or ""
            for name in ("name", "vat", "street", "zip", "city")
        } | {
            "state": self.partner_id.state_id.name or "",
            "country": self.partner_id.country_id.name or "",
        }
        values.update(
            {
                "contractual": contractual,
                "tractor_license_plate": self.tractor_license_plate_id.license_plate,
                "deca_notes": self.deca_notes,
                # Part of the DeCA hash: a change of vehicle is a new version,
                # even if the new vehicle has the same plate.
                "tractor_vehicle_id": self.tractor_license_plate_id.id,
                "trailer_vehicle_id": self.trailer_license_plate_id.id,
            }
        )
        if self.trailer_license_plate_id:
            values.update(
                {
                    "trailer_license_plate": (
                        self.trailer_license_plate_id.license_plate
                    ),
                }
            )
        for goods, move in zip(values["goods"], self.move_ids, strict=False):
            goods["upload_date"] = (
                move.upload_date.strftime("%d/%m/%Y") if move.upload_date else ""
            )
            goods["place_of_loading"] = move._partner_data_in_char_type(
                move.place_of_loading_id
            )
            goods["place_of_delivery"] = "\n".join(
                move._partner_data_in_char_type(delivery)
                for delivery in move.place_of_delivery_ids
            )
        values["carrier"]["autonomous"] = self.carrier_contact_id.autonomous
        return values
