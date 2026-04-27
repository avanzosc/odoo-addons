# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def find_sale_line_sequence_in_purchase_order(self, sale_line):
        line = self.order_line.filtered(lambda x: x.sequence == sale_line.sequence)
        if not line:
            vals = {
                "order_id": self.id,
                "sequence": sale_line.sequence,
                "name": sale_line.name,
                "sale_line_id": sale_line.id,
                "sale_order_id": sale_line.order_id.id,
                "display_type": sale_line.display_type,
                "product_qty": 0,
            }
            self.env["purchase.order.line"].create(vals)
