# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    qty_invoiced = fields.Float(
        compute="_compute_qty_invoiced",
        string="Billed Qty",
        digits="Product Unit of Measure",
    )
    qty_received = fields.Float(
        compute="_compute_qty_received",
        digits="Product Unit of Measure",
    )
    qty_ordered = fields.Float(
        compute="_compute_qty_ordered",
        string="Ordered Qty",
        digits="Product Unit of Measure",
    )

    @api.depends("order_line", "order_line.qty_invoiced")
    def _compute_qty_invoiced(self):
        for purchase in self:
            purchase.qty_invoiced = sum(purchase.order_line.mapped("qty_invoiced"))

    @api.depends("order_line", "order_line.qty_received")
    def _compute_qty_received(self):
        for purchase in self:
            purchase.qty_received = sum(purchase.order_line.mapped("qty_received"))

    @api.depends("order_line", "order_line.product_qty")
    def _compute_qty_ordered(self):
        for purchase in self:
            purchase.qty_ordered = sum(purchase.order_line.mapped("product_qty"))
