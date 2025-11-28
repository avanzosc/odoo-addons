# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import re

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def action_create_package(self, base_prefix=None):
        production = self.move_id.production_id
        if production:
            production.procurement_group_id._compute_packaged_finished_moves()
            pack_vals = {}
            normalized_procurement = "".join(
                re.findall(r"\d", production.procurement_group_id.name)
            )
            next_number = production.packaged_finished_moves + 1
            name = f"{normalized_procurement}-{next_number:02}"
            pack_vals.update({"name": name})
            package = self.env["stock.quant.package"].create(pack_vals)
            return package
        else:
            return super().action_create_package(base_prefix)
