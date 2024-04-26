# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def write(self, values):
        result = super().write(values)
        if "price_unit" in values and values.get("price_unit", False):
            for line in self.filtered(lambda x: x.move_id.type == "in_move"):
                product = line.mapped("product_id")
                if line.move_id.state in ("draft", "cancel"):
                    product.set_product_last_supplier_move()
                else:
                    product.set_product_last_supplier_move(line.move_id.id)
        return result
