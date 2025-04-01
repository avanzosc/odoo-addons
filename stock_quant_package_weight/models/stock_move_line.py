# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def write(self, vals):
        result = super().write(vals)
        if "result_package_id" in vals and vals.get("result_package_id"):
            for line in self.filtered(lambda x: x.result_package_id):
                line.result_package_id._compute_estimated_pack_weight_kg()
        return result
