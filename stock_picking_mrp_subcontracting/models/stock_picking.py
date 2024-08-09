# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    production_id = fields.Many2one(
        string="Manufacturing Order",
        comodel_name="mrp.production",
        compute="_compute_production_id",
        store=True,
        copy=False,
    )

    @api.depends(
        "move_ids", "move_ids.move_orig_ids", "move_ids.move_orig_ids.production_id"
    )
    def _compute_production_id(self):
        for picking in self:
            production_id = False
            for move in picking.move_ids:
                for origin_move in move.move_orig_ids.filtered(
                    lambda x: x.production_id
                ):
                    if not production_id:
                        production_id = origin_move.production_id.id
                        break
                if production_id:
                    break
            picking.production_id = production_id
