# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sequence = fields.Integer(
        compute="_compute_sequence", store=True, copy=False, readonly=True
    )

    @api.depends("sale_line_id", "sale_line_id.sequence")
    def _compute_sequence(self):
        for purchase in self:
            sequence = 0
            if purchase.sale_line_id:
                sequence = purchase.sale_line_id.sequence
            purchase.sequence = sequence

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if not line.sale_line_id and line.order_id.origin:
                line.put_sale_order_line()
        return lines

    def put_sale_order_line(self):
        cond = [("name", "=", self.order_id.origin)]
        sale = self.env["sale.order"].search(cond, limit=1)
        if sale:
            line = sale.order_line.filtered(
                lambda x: x.product_id == self.product_id
                and x.product_uom_qty == self.product_qty
            )
            if len(line) == 1:
                self.sale_line_id = line.id
