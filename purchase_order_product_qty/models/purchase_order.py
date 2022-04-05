# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_product_qty = fields.Float(
        string='Order Product Qty', compute='_compute_order_product_qty')

    def _compute_order_product_qty(self):
        for po in self:
            po.order_product_qty = sum(po.order_line.mapped('product_qty'))
