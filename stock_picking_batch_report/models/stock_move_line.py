# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sale_order_customer_reference = fields.Char(
        string="Sale order customer reference",
        compute="_compute_sale_order_customer_reference",
    )

    def _compute_sale_order_customer_reference(self):
        for line in self:
            customer_reference = ""
            if line.picking_id and line.picking_id.origin:
                cond = [("name", "=", line.picking_id.origin)]
                sale_order = self.env["sale.order"].search(cond, limit=1)
                if sale_order and sale_order.client_order_ref:
                    customer_reference = sale_order.client_order_ref
            line.sale_order_customer_reference = customer_reference
