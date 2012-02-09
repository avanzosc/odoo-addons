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

class split_move_select_list(osv.osv_memory):
    _name = 'split.move.select.list'
    _description = 'Split lot selection list'
 
    _columns = {
            'prodlot_id':fields.many2one('stock.production.lot', 'Lot'),
            'check': fields.boolean('Check'),
            'wizard_id': fields.many2one('split.move.select.wizard', 'Wizard'),
    }
split_move_select_list()

class split_move_select_wizard(osv.osv_memory):
    _name = 'split.move.select.wizard'
    _description = 'Split lot with a selection wizard'
 
    _columns = {
            'prodlot_list': fields.one2many('split.move.select.list', 'wizard_id', 'Lot List'),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        values = []
        if not context:
            context = {}
        lot_obj = self.pool.get('stock.production.lot')
        move_obj = self.pool.get('stock.move')
        for line in move_obj.browse(cr, uid, context['active_ids']):
            lot_ids = lot_obj.search(cr, uid, [('product_id', '=', line.product_id.id), ('name', 'like', line.location_id.name[0:3]), ('stock_available', '>', 0)])
            for lot_id in lot_ids:
                values.append({
                    'prodlot_id': lot_id,
                    'wizard_id': 1,
                })
            res = {
                'prodlot_list': values,
            }
        return res
    
    def split_selected_lots(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        inventory_id = context.get('inventory_id', False)
        prodlot_obj = self.pool.get('stock.production.lot')
        inventory_obj = self.pool.get('stock.inventory')
        move_obj = self.pool.get('stock.move')
        new_move = []
        for data in self.browse(cr, uid, ids, context=context):
            for move in move_obj.browse(cr, uid, context['active_ids'], context=context):
                move_qty = move.product_qty
                quantity_rest = move.product_qty
                uos_qty_rest = move.product_uos_qty
                new_move = []
                lines = []
                for lot in data.prodlot_list:
                    if lot.check:
                        lines.append(lot)
                if len(lines) > quantity_rest:
                    raise osv.except_osv(_('User error'), _('Too many lots selected !'))
#                lines = [l for l in data.prodlot_list if l]
                for line in lines:
                    quantity = 1
#                    if quantity <= 0 or move_qty == 0:
#                        continue
                    quantity_rest -= quantity
                    uos_qty = quantity / move_qty * move.product_uos_qty
                    uos_qty_rest = quantity_rest / move_qty * move.product_uos_qty
                    if quantity_rest < 0:
                        quantity_rest = quantity
                        break
                    default_val = {
                        'product_qty': quantity,
                        'invoice_qty': quantity,
                        'product_uos_qty': uos_qty,
                        'state': move.state
                    }
                    if quantity_rest > 0:
                        current_move = move_obj.copy(cr, uid, move.id, default_val, context=context)
                        if inventory_id and current_move:
                            inventory_obj.write(cr, uid, inventory_id, {'move_ids': [(4, current_move)]}, context=context)
                        new_move.append(current_move)

                    if quantity_rest == 0:
                        current_move = move.id
                    
                    prodlot_id = line.prodlot_id.id

                    move_obj.write(cr, uid, [current_move], {'prodlot_id': prodlot_id, 'state':move.state})

                    update_val = {}
                    if quantity_rest > 0:
                        update_val['product_qty'] = quantity_rest
                        update_val['invoice_qty'] = quantity_rest
                        update_val['product_uos_qty'] = uos_qty_rest
                        update_val['state'] = move.state
                        move_obj.write(cr, uid, [move.id], update_val)

        return {'type':'ir.actions.act_window_close'}
    
split_move_select_wizard()