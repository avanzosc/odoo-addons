# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from collections import OrderedDict

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_product_price(self):
        self.ensure_one()
        lines_dict = OrderedDict()
        lines = self.invoice_line_ids.filtered(lambda x: x.display_type == "product")
        lines = lines.sorted(
            lambda ln: (-ln.sequence, ln.date, ln.move_name, -ln.id), reverse=True
        )
        for line in lines:
            key = (line.product_id.id, line.price_unit)
            if key not in lines_dict:
                lines_dict[key] = {
                    "product_name": line.product_id.display_name,
                    "price_unit": line.price_unit,
                    "quantity": line.quantity,
                    "product_uom": line.product_uom_id.name,
                    "price_subtotal": line.price_subtotal,
                    "price_total": line.price_total,
                }
            else:
                lines_dict[key]["quantity"] += line.quantity
                lines_dict[key]["price_subtotal"] += line.price_subtotal
                lines_dict[key]["price_total"] += line.price_total
        lines_dict = list(lines_dict.values())
        return lines_dict
