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
            if move.move_dest_id:
                picking_list.append(move.move_dest_id.picking_id.id)
            stock_move_obj = self.env['stock.move']
            st_moves = stock_move_obj.search(
                [('product_id', '=', move.product_id.id),
                 ('location_id', '=', move.location_dest_id.id),
                 ('state', '=', 'confirmed')], order='date_expected')
            for st_move in st_moves:
                st_move.picking_id.action_assign()
                picking_list.append(st_move.picking_id.id)
        return list(set(picking_list))

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
