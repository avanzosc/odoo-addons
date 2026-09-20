# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_default_invoice = fields.Boolean(
        string="Default Invoice Address",
        help="Use this contact as the default invoice address.",
    )
    is_default_shipping = fields.Boolean(
        string="Default Delivery Address",
        help="Use this contact as the default delivery address.",
    )

    def _unset_other_defaults(self, field_name):
        for partner in self:
            if not partner[field_name]:
                continue
            commercial_partner = partner.commercial_partner_id
            if not commercial_partner:
                continue
            others = self.search(
                [
                    ("id", "!=", partner.id),
                    ("commercial_partner_id", "=", commercial_partner.id),
                    (field_name, "=", True),
                ]
            )
            if others:
                others.write({field_name: False})

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._unset_other_defaults("is_default_invoice")
        partners._unset_other_defaults("is_default_shipping")
        return partners

    def write(self, vals):
        res = super().write(vals)
        if "is_default_invoice" in vals:
            self._unset_other_defaults("is_default_invoice")
        if "is_default_shipping" in vals:
            self._unset_other_defaults("is_default_shipping")
        return res

    def _get_default_contact(self, field_name):
        self.ensure_one()
        commercial_partner = self.commercial_partner_id
        if not commercial_partner:
            return self
        default_contact = self.search(
            [
                ("commercial_partner_id", "=", commercial_partner.id),
                (field_name, "=", True),
            ],
            limit=1,
        )
        return default_contact

    def address_get(self, adr_pref=None):
        res = super().address_get(adr_pref=adr_pref)
        if not adr_pref:
            return res
        if isinstance(adr_pref, str):
            adr_pref = [adr_pref]
        if len(self) != 1:
            return res
        if "invoice" in adr_pref:
            default_invoice = self._get_default_contact("is_default_invoice")
            if default_invoice:
                res["invoice"] = default_invoice.id
        if "delivery" in adr_pref:
            default_shipping = self._get_default_contact("is_default_shipping")
            if default_shipping:
                res["delivery"] = default_shipping.id
        return res
