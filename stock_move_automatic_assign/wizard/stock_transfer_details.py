# -*- coding: utf-8 -*-
# (c) Copyright 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockTransferDetails(models.TransientModel):
    _inherit = 'stock.transfer_details'

    def _reserve_move(self, move):
        """ reserves products from a counterpart picking of a move
        @param product: Product to check to reserve
        @return: reserved stock_picking id
        """
        picking_list = []
        if move:
            stock_move_obj = self.env['stock.move']
            st_moves = stock_move_obj.search(
                [('product_id', '=', move.product_id.id),
                 ('location_id', '=', move.location_dest_id.id),
                 ('state', '=', 'confirmed')], order='date_expected')
            moves = st_moves | move.move_dest_id
            moves.action_assign()
            picking_list = moves.mapped('picking_id.id')
        return picking_list

    @api.multi
    def do_detailed_transfer(self):
        res = super(StockTransferDetails, self).do_detailed_transfer()
        picking_list = []
        if self.picking_id.picking_type_code == 'incoming':
            for move in self.picking_id.move_lines:
                picking_list += self._reserve_move(move)
            res = {'view_type': 'form',
                   'view_mode': 'tree,form',
                   'res_model': 'stock.picking',
                   'res_ids': list(set(picking_list)),
                   'domain': [('id', 'in', picking_list)],
                   'type': 'ir.actions.act_window'
                   }
        return res
