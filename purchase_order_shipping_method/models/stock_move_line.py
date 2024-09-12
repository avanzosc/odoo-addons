# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    shipping_cost = fields.Float(
        digits="Shipping Cost Decimal Precision",
    )
    picking_shipping_cost = fields.Float(
        string="Picking Shipping Cost",
        digits="Shipping Cost Decimal Precision",
        related="picking_id.shipping_cost",
        store=True,
    )

    @api.onchange("qty_done", "product_id", "picking_id")
    def onchange_shipping_cost(self):
        if (
            self.product_id
            and self.product_id.weight
            and (self.picking_id)
            and (self.picking_id.shipping_cost)
        ):
            self.shipping_cost = (self.product_id.weight * self.qty_done) * (
                self.picking_id.shipping_cost
            )
