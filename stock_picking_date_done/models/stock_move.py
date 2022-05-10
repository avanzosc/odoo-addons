# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self, cancel_backorder=False):
        done_moves = super(StockMove, self)._action_done(
            cancel_backorder=cancel_backorder)
        for move in done_moves:
            if move.picking_id.custom_date_done:
                move.date = move.picking_id.custom_date_done
        return done_moves
