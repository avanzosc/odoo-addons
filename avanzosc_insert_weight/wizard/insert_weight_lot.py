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

class mrp_weight_lot_list_wizard(osv.osv_memory):
    _name = 'mrp.weight.lot.list.wizard'
    _description = 'Wizard to optain lot list'
 
    _columns = {
            'lot_id': fields.many2one('stock.production.lot', 'Lot'),
            'weight': fields.float('Weight'),
            'wizard_id':fields.many2one('mrp.weight.wizard', 'Lot wizard'),
        }
    
    _defaults = {  
        'weight': lambda *a: 0.0,
    }
mrp_weight_lot_list_wizard()

class mrp_weight_wizard(osv.osv_memory):
    _name = 'mrp.weight.wizard'
    _description = 'Wizard to insert weight into lots'
 
    _columns = {
            'lot_list':fields.one2many('mrp.weight.lot.list.wizard', 'wizard_id', 'Lot list'),
        }
    
    def default_get(self, cr, uid, fields_list, context=None):
        values = {}
        res = {}
        lot_list = []
        for order in self.pool.get('mrp.production').browse(cr, uid, context['active_ids']):
            if order.state != 'done':
                raise osv.except_osv(_('User error'), _('The order is not done yet !'))
            for move in order.move_created_ids2:
                if move.product_id.track_production:
                    if move.prodlot_id:
                        values = {
                            'lot_id': move.prodlot_id.id,
                            'weight': move.prodlot_id.weight,
                        }
                        lot_list.append(values)
            res = {
                'lot_list': sorted(lot_list),
            }
        return res
    
    def insert_weight(self, cr, uid, ids, context=None):
        lot_obj = self.pool.get('stock.production.lot')
        for config in self.browse(cr, uid, ids):
            for item in config.lot_list:
                lot_obj.write(cr, uid, item.lot_id.id, {'weight': item.weight})
        return {'type': 'ir.actions.act_window_close'}
    
mrp_weight_wizard()