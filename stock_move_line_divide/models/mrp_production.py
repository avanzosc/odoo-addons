# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    packaged_finished_moves = fields.Integer(compute="_compute_packaged_finished_moves")

    @api.depends("procurement_group_id")
    def _compute_packaged_finished_moves(self):
        for production in self:
            if not production.procurement_group_id:
                production.packaged_finished_moves = 0
                continue
            related_productions = production.env["mrp.production"].search(
                [("procurement_group_id", "=", production.procurement_group_id.id)]
            )
            finished_lines = related_productions.mapped(
                "move_finished_ids.move_line_ids"
            ).filtered(
                lambda ml: ml.result_package_id
                and ml.product_id == production.product_id
            )
            production.packaged_finished_moves = len(finished_lines)

    def action_show_packaged_finished_moves(self):
        self.ensure_one()
        related_productions = self.env["mrp.production"].search(
            [("procurement_group_id", "=", self.procurement_group_id.id)]
        )
        finished_lines = related_productions.mapped(
            "move_finished_ids.move_line_ids"
        ).filtered(lambda ml: ml.result_package_id and ml.product_id == self.product_id)
        return {
            "type": "ir.actions.act_window",
            "name": "Packaged Finished Move Lines",
            "view_mode": "tree",
            "res_model": "stock.move.line",
            "domain": [("id", "in", finished_lines.ids)],
            "context": {"default_procurement_group_id": self.procurement_group_id.id},
        }
