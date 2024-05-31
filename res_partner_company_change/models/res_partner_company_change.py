# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
from babel.util import distinct


class ResPartnerCompanyChange(models.Model):
    _name = "res.partner.company.change"
    _inherit = "base.import"
    _description = "Wizard to change company to contacts"

    import_line_ids = fields.One2many(
        comodel_name="res.partner.company.change.line",
        copy=True,
    )
    contact_count = fields.Integer(
        string="# Conatcts",
        compute="_compute_contact_count",
    )
    company_origin_id = fields.Many2one(
        comodel_name="res.company",
        string="Origin Company",
        index=True,
        required=True,
    )
    company_dest_id = fields.Many2one(
        comodel_name="res.company",
        string="Company Dest",
        index=True,
        required=True,
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name="res.country",
        index=True,
        required=True,
    )
    property_account_position_id = fields.Many2one(
        string="Fiscal Position",
        comodel_name="account.fiscal.position",
        index=True,
        required=True,
    )
    data = fields.Binary(
        required=False,
    )

    def _compute_contact_count(self):
        for record in self:
            record.contact_count = len(
                record.mapped("import_line_ids.partner_id")
            )

    def button_open_partner(self):
        self.ensure_one()
        contacts = self.mapped("import_line_ids.partner_id")
        action = self.env.ref("contacts.action_contacts")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", contacts.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def button_open_import_line(self):
        self.ensure_one()
        action_dict = super(
            ResPartnerCompanyChange, self
        ).button_open_import_line()
        tree_view_id = self.env.ref(
            "res_partner_company_change.res_partner_company_change_line_view_tree"
        ).id
        action_dict.update({
            "views": [[tree_view_id, "tree"], [False, "form"]],
        })
        return action_dict

    def _read_file(self):
        if self.data:
            return super()._read_file()
        lines = []
        partner_sudo = self.sudo().env["res.partner"]
        contacts = partner_sudo.search([
            ("company_id", "=", self.company_origin_id.id),
            ("country_id", "=", self.country_id.id),
            ('is_company', '=', True)
        ])
        contacts |= partner_sudo.search([("parent_id", "in", contacts.ids)])
        for contact in contacts:
            origin_contact = contact.with_context(
                force_company=self.company_origin_id.id)
            line_data = {
                "import_id": self.id,
                "partner_id": origin_contact.id,
                "property_account_position_id": (
                    self.property_account_position_id.id
                ),
                "customer_payment_mode_name":
                    origin_contact.customer_payment_mode_id.name,
                "supplier_payment_mode_name":
                    origin_contact.supplier_payment_mode_id.name,
                "delivery_carrier_name":
                    origin_contact.property_delivery_carrier_id.name,
                "payment_term_name":
                    origin_contact.property_payment_term_id.name,
                "supplier_payment_term_name":
                    origin_contact.property_supplier_payment_term_id.name,
            }
            lines.append((0, 0, line_data))
        return lines


class ResPartnerCompanyChangeLine(models.Model):
    _name = "res.partner.company.change.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to change company to contacts"

    import_id = fields.Many2one(
        comodel_name="res.partner.company.change",
    )
    action = fields.Selection(
        selection_add=[
            ("update", "Update"),
        ],
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    property_account_position_id = fields.Many2one(
        string="Fiscal Position",
        comodel_name="account.fiscal.position",
    )
    customer_payment_mode_name = fields.Char()
    supplier_payment_mode_name = fields.Char()
    delivery_carrier_name = fields.Char()
    payment_term_name = fields.Char()
    supplier_payment_term_name = fields.Char()
    customer_payment_mode_id = fields.Many2one(
        string="Customer Payment Mode",
        comodel_name="account.payment.mode",
    )
    supplier_payment_mode_id = fields.Many2one(
        string="Supplier Payment Mode",
        comodel_name="account.payment.mode",
    )
    property_delivery_carrier_id = fields.Many2one(
        string="Delivery Carrier",
        comodel_name="delivery.carrier",
    )
    property_payment_term_id = fields.Many2one(
        string="Customer Payment Term",
        comodel_name="account.payment.term",
    )
    property_supplier_payment_term_id = fields.Many2one(
        string="Supplier Payment Term",
        comodel_name="account.payment.term",
    )
    current_partner_company_id = fields.Many2one(
        comodel_name="res.company",
        related="partner_id.company_id",
    )

    def _action_validate(self):
        self.ensure_one()
        update_values = super()._action_validate()
        log_infos = []
        customer_payment_mode = supplier_payment_mode = delivery_carrier = False
        property_payment_term = property_supplier_payment_term = False
        partner_company = self.partner_id.with_context(
            force_company=self.import_id.company_dest_id.id)
        customer_payment_mode_name = (self.customer_payment_mode_name or
                                      partner_company.customer_payment_mode_id.name)
        if customer_payment_mode_name:
            customer_payment_mode, log_info_customer_payment_mode = (
                self._check_customer_payment_mode(customer_payment_mode_name)
            )
            if log_info_customer_payment_mode:
                log_infos.append(log_info_customer_payment_mode)
        supplier_payment_mode_name = (self.supplier_payment_mode_name or
                                      partner_company.supplier_payment_mode_id.name)
        if supplier_payment_mode_name:
            supplier_payment_mode, log_info_supplier_payment_mode = (
                self._check_supplier_payment_mode(supplier_payment_mode_name)
            )
            if log_info_supplier_payment_mode:
                log_infos.append(log_info_supplier_payment_mode)
        delivery_carrier_name = (self.delivery_carrier_name or
                                 partner_company.property_delivery_carrier_id.name)
        if delivery_carrier_name:
            delivery_carrier, log_info_delivery_carrier = (
                self._check_delivery_carrier(delivery_carrier_name)
            )
            if log_info_delivery_carrier:
                log_infos.append(log_info_delivery_carrier)
        payment_term_name = (self.payment_term_name or
                             partner_company.property_payment_term_id.name)
        if payment_term_name:
            property_payment_term, log_info_property_payment_term = (
                self._check_property_payment_term(payment_term_name)
            )
            if log_info_property_payment_term:
                log_infos.append(log_info_property_payment_term)
        supplier_payment_term_name = (
            self.supplier_payment_term_name or
            partner_company.property_supplier_payment_term_id.name
        )
        if supplier_payment_term_name:
            (
                property_supplier_payment_term,
                log_info_property_supplier_payment_term
            ) = self._check_property_supplier_payment_term(supplier_payment_term_name)
            if log_info_property_supplier_payment_term:
                log_infos.append(log_info_property_supplier_payment_term)
        state = "error" if log_infos else "pass"
        action = "update" if state != "error" else "nothing"
        update_values.update(
            {
                "customer_payment_mode_name": (
                    customer_payment_mode_name or self.customer_payment_mode_name
                ),
                "customer_payment_mode_id": (
                    customer_payment_mode and customer_payment_mode.id
                ),
                "supplier_payment_mode_name": (
                    supplier_payment_mode_name or self.supplier_payment_mode_name
                ),
                "supplier_payment_mode_id": (
                    supplier_payment_mode and supplier_payment_mode.id
                ),
                "delivery_carrier_name": (
                    delivery_carrier_name or self.delivery_carrier_name
                ),
                "property_delivery_carrier_id": (
                    delivery_carrier and delivery_carrier.id
                ),
                "payment_term_name": (
                    payment_term_name or self.payment_term_name
                ),
                "property_payment_term_id": (
                    property_payment_term and property_payment_term.id
                ),
                "supplier_payment_term_name": (
                    supplier_payment_term_name or self.supplier_payment_term_name
                ),
                "property_supplier_payment_term_id": (
                    property_supplier_payment_term
                ) and property_supplier_payment_term.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        self.ensure_one()
        update_values = super()._action_process()
        state = self.state
        if self.action == "update":
            self._update_company()
            self._update_values()
            state = "done"
        update_values.update(
            {
                "state": state,
            }
        )
        return update_values

    def _check_customer_payment_mode(self, payment_mode_name):
        self.ensure_one()
        log_info = ""
        customer_payment_mode_obj = self.sudo().env["account.payment.mode"]
        search_domain = [
            ("name", "=", payment_mode_name),
            ("company_id", "=", self.import_id.company_dest_id.id),
            ("payment_type", "=", "inbound"),
        ]
        customer_payment_mode = customer_payment_mode_obj.search(
            search_domain
        )
        if not customer_payment_mode:
            log_info = _("No customer payment mode found.")
        elif len(customer_payment_mode) > 1:
            customer_payment_mode = False
            log_info = _(
                "More than one customer payment mode found."
            )
        return customer_payment_mode and customer_payment_mode[:1], log_info

    def _check_supplier_payment_mode(self, supplier_payment_mode_name):
        self.ensure_one()
        log_info = ""
        supplier_payment_mode_obj = self.sudo().env["account.payment.mode"]
        search_domain = [
            ("name", "=", supplier_payment_mode_name),
            ("company_id", "=", self.import_id.company_dest_id.id),
            ("payment_type", "=", "outbound"),
        ]
        supplier_payment_mode = supplier_payment_mode_obj.search(
            search_domain
        )
        if not supplier_payment_mode:
            log_info = _("No supplier payment mode found.")
        elif len(supplier_payment_mode) > 1:
            supplier_payment_mode = False
            log_info = _(
                "More than one supplier payment mode found."
            )
        return supplier_payment_mode and supplier_payment_mode[:1], log_info

    def _check_delivery_carrier(self, delivery_carrier_name):
        self.ensure_one()
        log_info = ""
        delivery_carrier_obj = self.sudo().env["delivery.carrier"]
        search_domain = [
            ("name", "=", delivery_carrier_name),
            ("company_id", "=", self.import_id.company_dest_id.id)
        ]
        delivery_carrier = delivery_carrier_obj.search(search_domain)
        if not delivery_carrier:
            log_info = _("No delivery carrier found.")
        elif len(delivery_carrier) > 1:
            delivery_carrier = False
            log_info = _(
                "More than one delivery carrier found."
            )
        return delivery_carrier and delivery_carrier[:1], log_info

    def _check_property_payment_term(self, payment_term_name):
        self.ensure_one()
        log_info = ""
        payment_term_obj = self.sudo().env["account.payment.term"]
        search_domain = [
            ("name", "=", payment_term_name),
            ("company_id", "=", self.import_id.company_dest_id.id)
        ]
        property_payment_term = payment_term_obj.search(
            search_domain
        )
        if not property_payment_term:
            log_info = _("No property payment term found.")
        elif len(property_payment_term) > 1:
            property_payment_term = False
            log_info = _(
                "More than one property payment term found."
            )
        return property_payment_term and property_payment_term[:1], log_info

    def _check_property_supplier_payment_term(self, payment_term_name):
        self.ensure_one()
        log_info = ""
        payment_term_obj = self.sudo().env["account.payment.term"]
        search_domain = [
            ("name", "=", payment_term_name),
            ("company_id", "=", self.import_id.company_dest_id.id)
        ]
        property_supplier_payment_term = payment_term_obj.search(search_domain)
        if not property_supplier_payment_term:
            log_info = _("No property supplier payment term found.")
        elif len(property_supplier_payment_term) > 1:
            property_supplier_payment_term = False
            log_info = _(
                "More than one property supplier payment term found."
            )
        return (
            property_supplier_payment_term
        ) and property_supplier_payment_term[:1], log_info

    def _update_company(self):
        self.ensure_one()
        if self.sudo().partner_id.user_id:
            self.partner_id.sudo().user_id.write({
                "company_ids": [(4, self.import_id.company_dest_id.id)],
                "company_id": self.import_id.company_dest_id.id,
            })

    def _update_values(self):
        self.ensure_one()
        vals = self._get_update_values()
        self.sudo().with_context(
            force_company=self.import_id.company_dest_id.id).partner_id.write(vals)

    def _get_update_values(self):
        return {
            "customer_payment_mode_id": self.customer_payment_mode_id.id,
            "supplier_payment_mode_id": self.supplier_payment_mode_id.id,
            "property_delivery_carrier_id": (
                self.property_delivery_carrier_id.id
            ),
            "property_payment_term_id": self.property_payment_term_id.id,
            "property_supplier_payment_term_id": (
                self.property_supplier_payment_term_id.id
            ),
            "company_id": self.import_id.company_dest_id.id,
        }
