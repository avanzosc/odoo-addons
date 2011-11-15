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
    
    def split(self, cr, uid, ids, move_ids, context=None):
        """ To split stock moves into production lot
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: the ID or list of IDs if we want more than one
        @param move_ids: the ID or list of IDs of stock move we want to split
        @param context: A standard dictionary
        @return:
        """
        if context is None:
            context = {}
        inventory_id = context.get('inventory_id', False)
        prodlot_obj = self.pool.get('stock.production.lot')
        inventory_obj = self.pool.get('stock.inventory')
        move_obj = self.pool.get('stock.move')
        new_move = []
        for data in self.browse(cr, uid, ids, context=context):
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                move_qty = move.product_qty
                quantity_rest = move.product_qty
                uos_qty_rest = move.product_uos_qty
                new_move = []
                if data.use_exist:
                    lines = [l for l in data.line_exist_ids if l]
                else:
                    lines = [l for l in data.line_ids if l]
                for line in lines:
                    quantity = line.quantity
                    if quantity <= 0 or move_qty == 0:
                        continue
                    quantity_rest -= quantity
                    uos_qty = quantity / move_qty * move.product_uos_qty
                    uos_qty_rest = quantity_rest / move_qty * move.product_uos_qty
                    if quantity_rest < 0:
                        quantity_rest = quantity
                        break
                    default_val = {
                        'product_qty': quantity,
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
                    prodlot_id = False
                    if data.use_exist:
                        prodlot_id = line.prodlot_id.id
                    if not prodlot_id:
                        prodlot_id = prodlot_obj.create(cr, uid, {
                            'prefix': line.prefix,
                            'name': line.name,
                            'product_id': move.product_id.id},
                        context=context)

                    move_obj.write(cr, uid, [current_move], {'prodlot_id': prodlot_id, 'state':move.state})

                    update_val = {}
                    if quantity_rest > 0:
                        update_val['product_qty'] = quantity_rest
                        update_val['product_uos_qty'] = uos_qty_rest
                        update_val['state'] = move.state
                        move_obj.write(cr, uid, [move.id], update_val)

        return new_move
split_in_production_lot()

class stock_move_split_lines(osv.osv_memory):
    _inherit='stock.move.split.lines'
    
    _columns = {
        'prefix': fields.char('Prefix', size=64), 
    }
    
stock_move_split_lines()

class stock_inventory_line_split(osv.osv_memory):
    _inherit='stock.inventory.line.split'
    
    def split(self, cr, uid, ids, line_ids, context=None):             
        prodlot_obj = self.pool.get('stock.production.lot')
        ir_sequence_obj = self.pool.get('ir.sequence')
        line_obj = self.pool.get('stock.inventory.line')
        new_line = []        
        for data in self.browse(cr, uid, ids, context=context):
            for inv_line in line_obj.browse(cr, uid, line_ids, context=context):
                line_qty = inv_line.product_qty
                quantity_rest = inv_line.product_qty                
                new_line = []   
                if data.use_exist:
                    lines = [l for l in data.line_exist_ids if l]
                else:
                    lines = [l for l in data.line_ids if l]                         
                for line in lines:
                    quantity = line.quantity
                    if quantity <= 0 or line_qty == 0:
                        continue
                    quantity_rest -= quantity
                    if quantity_rest < 0:
                        break
                                       
                    default_val = {
                        'product_qty': quantity,                         
                    }
                    prodlot_id = False
                    if data.use_exist:
                        prodlot_id = line.prodlot_id.id
                    if not prodlot_id:
                        prodlot_id = prodlot_obj.create(cr, uid, {
                            'prefix': line.prefix,
                            'name': line.name,
                            'product_id': inv_line.product_id.id},
                        context=context)
                        
                    if quantity_rest == 0:
                        new_line.append(inv_line.id)
                        line_obj.write(cr, uid, [inv_line.id], {'prod_lot_id': prodlot_id})
                        break
                        
                    current_line = line_obj.copy(cr, uid, inv_line.id, default_val)
                    new_line.append(current_line)
                    line_obj.write(cr, uid, [current_line], {'prod_lot_id': prodlot_id})                  
                    
                    update_val = {}
                    if quantity_rest > 0:                        
                        update_val['product_qty'] = quantity_rest                                            
                        line_obj.write(cr, uid, [inv_line.id], update_val)
                    
        return new_line

stock_inventory_line_split()