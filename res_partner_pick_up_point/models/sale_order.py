from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        if self.partner_id.pick_up_point_id:
            self.partner_shipping_id = self.partner_id.pick_up_point_id
        else:
            super().onchange_partner_id()

    @api.model
    def create(self, values):
        if "partner_id" in values and not values.get("partner_shipping_id"):
            partner_id = self.env["res.partner"].browse(values["partner_id"])
            if partner_id.pick_up_point_id:
                values["partner_shipping_id"] = partner_id.pick_up_point_id.id
        return super().create(values)

    def write(self, values):
        if "partner_id" in values and "partner_shipping_id" not in values:
            partner_id = self.env["res.partner"].browse(values["partner_id"])
            if partner_id.pick_up_point_id:
                values["partner_shipping_id"] = partner_id.pick_up_point_id.id
        return super().write(values)
