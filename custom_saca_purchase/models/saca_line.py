# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    purchase_order_id = fields.Many2one(
        string="Purchase Order",
        comodel_name="purchase.order")
    purchase_order_line_id = fields.Many2one(
        string="Purchase Orden Line",
        comodel_name="purchase.order.line")

    @api.onchange("purchase_price")
    def onchange_purchase_price(self):
        if self.purchase_price and (
            self.purchase_order_line_id) and (
                self.purchase_order_id.state) not in ("done", "cancel"):
            self.purchase_order_line_id.write(
                {"price_unit": self.purchase_price})

    def action_purchase_line(self, purchase_order):
        self.ensure_one()
        vals = {
            "name": u"{} {} {}".format(
                purchase_order.name, self.saca_id.name,
                self.vehicle_id.name),
            "product_id": self.saca_id.product_id.id,
            "product_qty": self.estimated_burden,
            "price_unit": self.purchase_price,
            "order_id": purchase_order.id,
            "saca_line_id": self.id,
            "saca_id": self.saca_id.id}
        purchase_line = self.env["purchase.order.line"].create(vals)
        self.purchase_order_line_id = purchase_line.id
