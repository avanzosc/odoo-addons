# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def write(self, values):
        result = super().write(values)
        lines = self.filtered(
            lambda x: x.display_type == "product"
            and x.move_id
            and x.move_id.move_type == "in_invoice"
        )
        if lines and "balance" in values and values.get("balance", False):
            for line in lines:
                product = line.mapped("product_id")
                if line.move_id.state in ("draft", "cancel"):
                    product.set_product_last_supplier_move()
                else:
                    product.set_product_last_supplier_move(line.move_id.id)
        return result
