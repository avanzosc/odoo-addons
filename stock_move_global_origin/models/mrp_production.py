# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    global_origin = fields.Char(compute="_compute_global_origin", store=True)

    @api.depends("move_finished_ids.move_dest_ids.global_origin")
    def _compute_global_origin(self):
        for production in self:
            downstream_origins = production.move_finished_ids.move_dest_ids.mapped(
                "global_origin"
            )
            production.global_origin = next(
                (origin for origin in downstream_origins if origin), False
            )
