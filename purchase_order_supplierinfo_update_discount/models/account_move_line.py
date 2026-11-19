# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def write(self, vals):
        result = super().write(vals)
        if "balance" in vals:
            lines = self.filtered(
                lambda x: x.product_id
                and x.display_type == "product"
                and x.move_id.move_type == "in_invoice"
                and x.purchase_line_id
            )
            for line in lines:
                line.purchase_line_id.write(
                    {"price_unit": line.price_unit, "discount": line.discount}
                )
        return result
