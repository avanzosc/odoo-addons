# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    qty_to_invoice = fields.Float(
        compute="_compute_qty_to_invoice",
        search="_search_qty_to_invoice",
        string="Qty to Bill",
        default=0.0,
    )
    qty_to_receive = fields.Float(
        compute="_compute_qty_to_receive",
        search="_search_qty_to_receive",
        string="Qty to Receive",
        default=0.0,
    )

    @api.model
    def _search_qty_to_invoice(self, operator, value):
        value = float(value) if value else 0.0
        po_line_obj = self.env["purchase.order.line"]
        cond = [("qty_to_invoice", operator, value)]
        po_lines = po_line_obj.search(cond)
        orders = po_lines.mapped("order_id")
        return [("id", "in", orders.ids)]

    @api.model
    def _search_qty_to_receive(self, operator, value):
        value = float(value) if value else 0.0
        po_line_obj = self.env["purchase.order.line"]
        cond = [("qty_to_receive", operator, value)]
        po_lines = po_line_obj.search(cond)
        orders = po_lines.mapped("order_id")
        return [("id", "in", orders.ids)]
