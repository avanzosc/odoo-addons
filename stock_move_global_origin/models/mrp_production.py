# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    global_origin = fields.Char(
        compute="_compute_global_origin", store=True, index=True, recursive=True
    )

    @api.depends(
        "move_finished_ids.move_dest_ids.global_origin",
        "move_finished_ids.move_dest_ids.production_id",
    )
    def _compute_global_origin(self):
        for production in self:
            demand_moves = production.move_finished_ids.move_dest_ids.filtered(
                lambda move, production=production: move.production_id != production
                and move._is_global_origin_demand()
            )
            production.global_origin = next(
                (origin for origin in demand_moves.mapped("global_origin") if origin),
                False,
            )
