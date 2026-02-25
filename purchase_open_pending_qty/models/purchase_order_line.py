# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    pending_qty_to_invoice = fields.Float(
        compute="_compute_pending_qty_custom",
        string="Pendiente de facturar",
        store=True,
        digits="Product Unit of Measure",
    )
    pending_qty_to_receive = fields.Float(
        compute="_compute_pending_qty_custom",
        string="Pendiente de recibir",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends("qty_to_invoice", "qty_invoiced", "qty_to_receive", "qty_received")
    def _compute_pending_qty_custom(self):
        for line in self:
            line.pending_qty_to_invoice = line.qty_to_invoice - line.qty_invoiced
            line.pending_qty_to_receive = line.qty_to_receive - line.qty_received

    def copy_purchase_order_line(self):
        for line in self:
            line.copy(
                {
                    "name": line.name,
                    "order_id": line.order_id.id,
                    "product_id": line.product_id.id,
                }
            )
