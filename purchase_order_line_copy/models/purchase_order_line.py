# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.multi
    def copy_purchase_order_line(self):
        for line in self:
            line.copy(
                {'name': line.name,
                 'order_id': line.order_id.id,
                 'product_id': line.product_id.id,
                 })
