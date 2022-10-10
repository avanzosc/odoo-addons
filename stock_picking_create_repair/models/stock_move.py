# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    is_repair = fields.Boolean(
        string="It's repair", store=True, copy=False,
        related="picking_id.is_repair")

    def _action_done(self, cancel_backorder=False):
        if "move_no_to_done" in self.env.context:
            return self.env['stock.move']
        else:
            return super(StockMove, self)._action_done(
                cancel_backorder=cancel_backorder)
