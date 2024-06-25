# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    qty_invoiced = fields.Float(
        compute="_compute_qty_invoiced",
        string="Qty Billed",
    )
    qty_received = fields.Float(
        compute="_compute_qty_received",
        string="Qty Received",
    )

    @api.depends("order_line", "order_line.qty_invoiced")
    def _compute_qty_invoiced(self):
        for purchase in self:
            qty_invoiced = 0
            if purchase.order_line:
                qty_invoiced = sum(purchase.order_line.mapped("qty_invoiced"))
            purchase.qty_invoiced = qty_invoiced

    @api.depends("order_line", "order_line.qty_received")
    def _compute_qty_received(self):
        for purchase in self:
            qty_received = 0
            if purchase.order_line:
                qty_received = sum(purchase.order_line.mapped("qty_received"))
            purchase.qty_received = qty_received
