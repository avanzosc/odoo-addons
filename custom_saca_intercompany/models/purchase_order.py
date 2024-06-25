# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    total_qty = fields.Float(
        string="Total Qty", compute="_compute_total_qty", store=True
    )

    @api.depends("order_line", "order_line.qty_received")
    def _compute_total_qty(self):
        for purchase in self:
            total_qty = 0
            if purchase.order_line:
                total_qty = sum(purchase.order_line.mapped("qty_received"))
            purchase.total_qty = total_qty

    def _prepare_sale_order_data(
        self, name, partner, dest_company, direct_delivery_address
    ):
        result = super()._prepare_sale_order_data(
            name, partner, dest_company, direct_delivery_address
        )
        if self.saca_line_id:
            result.update({"saca_line_id": self.saca_line_id.id})
            if self.saca_line_id.breeding_id.location_id.warehouse_id:
                result.update(
                    {
                        "warehouse_id": (
                            self.saca_line_id.breeding_id.location_id.warehouse_id.id
                        )
                    }
                )
        return result
