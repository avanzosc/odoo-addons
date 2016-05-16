# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _find_moves_from_stock_information(
        self, company, to_date, from_date=None, category=None, template=None,
        products=None, location_id=None, location_dest_id=None, periods=True,
            without_reservation=True):
        reservation_obj = self.env['stock.reservation']
        moves = super(StockMove, self)._find_moves_from_stock_information(
            company, to_date, from_date=from_date, category=category,
            template=template, products=products, location_id=location_id,
            location_dest_id=location_dest_id)
        if periods:
            return moves
        final_moves = self.env['stock.move']
        for move in moves:
            cond = [('move_id', '=', move.id)]
            reservation = reservation_obj.search(cond, limit=1)
            if without_reservation and not reservation:
                final_moves |= move
            elif not without_reservation and reservation:
                final_moves |= move
        return final_moves
