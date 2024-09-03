from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def onchange_delivery_point_partner_id(self):
        if self.partner_id.delivery_point:
            self.partner_shipping_id = self.partner_id.delivery_point

    @api.model
    def create(self, values):
        if "partner_id" in values and not values.get("partner_shipping_id"):
            partner_id = self.env["res.partner"].browse(values["partner_id"])
            if partner_id.delivery_point:
                values["partner_shipping_id"] = partner_id.delivery_point.id
        return super().create(values)

    def write(self, values):
        if "partner_id" in values and "partner_shipping_id" not in values:
            partner_id = self.env["res.partner"].browse(values["partner_id"])
            if partner_id.delivery_point:
                values["partner_shipping_id"] = partner_id.delivery_point.id
        return super().write(values)
