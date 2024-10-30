import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockReplenishment(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_in_kits = fields.Float(
        string="Qty Kit",
        related="product_id.qty_in_kits",
        readonly=True,
    )

    def button_assign_qty_in_orderpoint(self):
        for orderpoint in self:
            product = orderpoint.product_id
            orderpoint.qty_to_order = (
                product.qty_in_kits
                + orderpoint.outgoing_qty2
                + orderpoint.outgoing_qty
                - (orderpoint.qty_on_hand + orderpoint.incoming_qty)
            )

    def button_calculate_qty_in_kits(self):
        for orderpoint in self:
            try:
                orderpoint.product_id.button_calculate_qty_in_kits()
            except Exception as e:
                _logger.error(
                    "Error calculating qty in kits for product %s: %s",
                    orderpoint.product_id.name,
                    e,
                )
