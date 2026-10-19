# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        self.ensure_one()
        sorted_lines = []
        lines = super().lines_grouped_by_picking()
        for item in lines:
            if "picking" in item and item.get("picking"):
                sorted_lines.append(item)
        for item in lines:
            if "picking" in item and not item.get("picking"):
                sorted_lines.append(item)
        return sorted_lines
