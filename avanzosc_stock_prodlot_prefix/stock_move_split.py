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

class split_in_production_lot(osv.osv_memory):
    _inherit = 'stock.move.split'
 
    def split_lot(self, cr, uid, ids, context=None):
        values = {}
        stock_move_obj = self.pool.get('stock.move')
        prodlot_obj = self.pool.get('stock.production.lot')
        super(split_in_production_lot, self).split_lot(cr, uid, ids, context)
        for wizard in self.browse(cr, uid, ids):
            for line in wizard.line_ids:
                for move in stock_move_obj.browse(cr, uid, context.get('active_ids')):
                    if line.prefix and line.name == move.prodlot_id.name:
                        values = {
                            'prefix': line.prefix,
                        }
                    prodlot_obj.write(cr, uid, [move.prodlot_id.id], values)
        return {'type': 'ir.actions.act_window_close'}
split_in_production_lot()

class stock_move_split_lines(osv.osv_memory):
    _inherit='stock.move.split.lines'
    
    _columns = {
        'prefix': fields.char('Prefix', size=64), 
    }
    
stock_move_split_lines()