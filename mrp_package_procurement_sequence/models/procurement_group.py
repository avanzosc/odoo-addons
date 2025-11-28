# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    packaged_finished_moves = fields.Integer(compute="_compute_packaged_finished_moves")

    @api.depends("mrp_production_ids.move_finished_ids.move_line_ids")
    def _compute_packaged_finished_moves(self):
        for group in self:
            total = 0
            for production in group.mrp_production_ids:
                product = production.product_id
                move_lines = production.move_finished_ids.move_line_ids.filtered(
                    lambda ml: ml.product_id == product
                )
                total += len(move_lines.filtered(lambda ml: ml.result_package_id))
            group.packaged_finished_moves = total
