# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields
from tools.translate import _

class stock_move(osv.osv):
    _inherit = 'stock.move'
 
    _columns = {
        'line_weight': fields.related('prodlot_id', 'weight', type='float', string='Line Weight'),
    }
    
    def onchange_prodlot_id(self, cr, uid, ids, context=None):
        value = {}
        for move in self.browse(cr, uid, ids):
            if move.prodlot_id.weight > 0:
                value = {
                    'invoice_qty': move.prodlot_id.weight,
                }
        return {'value': value}
stock_move()

class split_in_production_lot(osv.osv_memory):
    _inherit = "stock.move.split"
    
    def split_lot(self, cr, uid, ids, context=None):
        """ To split a lot
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: An ID or list of IDs if we want more than one
        @param context: A standard dictionary
        @return:
        """
        stock_move_obj = self.pool.get('stock.move')
        if context is None:
            context = {}
        ids = self.split(cr, uid, ids, context.get('active_ids'), context=context)
        for move in stock_move_obj.browse(cr, uid, ids):
            if move.prodlot_id.weight > 0:
                stock_move_obj.write(cr, uid, move.id, {'invoice_qty': move.prodlot_id.weight})
                for old_move in stock_move_obj.browse(cr, uid, context.get('active_ids')):
                    if not old_move.prodlot_id:
                        stock_move_obj.write(cr, uid, old_move.id, {'invoice_qty': old_move.product_qty})
                    else:
                        stock_move_obj.write(cr, uid, old_move.id, {'invoice_qty': old_move.prodlot_id.weight})
        for move in stock_move_obj.browse(cr, uid, context.get('active_ids')):
            if not ids and move.prodlot_id.weight > 0:
                stock_move_obj.write(cr, uid, move.id, {'invoice_qty': move.prodlot_id.weight})
        return {'type': 'ir.actions.act_window_close'}
    
split_in_production_lot()