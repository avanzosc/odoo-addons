# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    partner_supplierinfo_delivery_delay = fields.Integer(
        string="Vendor Delivery Delay",
        related="partner_id.supplierinfo_delivery_delay",
    )
    delivery_delay_differs = fields.Boolean(
        string="Delivery Lead Time Differs",
        compute="_compute_delivery_delay_differs",
        store=True,
    )

    @api.depends("delay", "partner_id.supplierinfo_delivery_delay")
    def _compute_delivery_delay_differs(self):
        for supplierinfo in self:
            partner_delay = supplierinfo.partner_supplierinfo_delivery_delay
            supplierinfo.delivery_delay_differs = (
                bool(partner_delay) and supplierinfo.delay != partner_delay
            )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        self._apply_partner_delivery_delay()
        return result

    @api.model_create_multi
    def create(self, vals_list):
        partner_ids = {
            vals["partner_id"] for vals in vals_list if vals.get("partner_id")
        }
        partners = self.env["res.partner"].browse(partner_ids)
        partner_delay_by_id = {
            partner.id: partner.supplierinfo_delivery_delay for partner in partners
        }
        for vals in vals_list:
            partner_delay = partner_delay_by_id.get(vals.get("partner_id"))
            if partner_delay and vals.get("delay") != partner_delay:
                vals["delay"] = partner_delay
        return super().create(vals_list)

    def action_assign_partner_delivery_delay(self):
        self._apply_partner_delivery_delay()

    def _apply_partner_delivery_delay(self):
        for supplierinfo in self:
            partner_delay = supplierinfo.partner_supplierinfo_delivery_delay
            if partner_delay and supplierinfo.delay != partner_delay:
                supplierinfo.delay = partner_delay
