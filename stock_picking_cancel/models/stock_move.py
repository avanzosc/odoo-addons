# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def do_cancel_done(self):
        for move in self:
            move.state = 'draft'
            for move_line in move.move_line_ids:
                move_line._refresh_quants_by_picking_cancelation()
            move._do_unreserve()
            move.move_line_ids.unlink()
