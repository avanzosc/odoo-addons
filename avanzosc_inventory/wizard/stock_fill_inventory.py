# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from osv import fields, osv
from tools.translate import _
import netsvc
import tools
import decimal_precision as dp
import logging
class stock_fill_inventory(osv.osv_memory):
    
    _inherit ='stock.fill.inventory'
    
    _columns={
              'categ_id':fields.many2one('product.category', 'Category'),
              }
    def fill_inventory(self, cr, uid, ids, context=None):
        """ To Import stock inventory according to products available in the selected locations.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: the ID or list of IDs if we want more than one
        @param context: A standard dictionary
        @return:
        """
        if context is None:
            context = {}

        inventory_line_obj = self.pool.get('stock.inventory.line')
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        move_obj = self.pool.get('stock.move')
        inv_obj = self.pool.get('stock.inventory')
        category_obj = self.pool.get('product.category')
        
        inventory = inv_obj.browse(cr,uid,context.get('active_ids',[]))[0]
        fill_inventory = self.browse(cr, uid, ids[0], context=context)
        res = {}
        res_location = {}
        product_context=dict(context)
        
        if fill_inventory.recursive:
            location_ids = location_obj.search(cr, uid, [('location_id',
                             'child_of', [fill_inventory.location_id.id])],context=context)
        else:
            location_ids = [fill_inventory.location_id.id]
        
        product_list=[]
        categ_list = []
        if fill_inventory.categ_id:
            categ = fill_inventory.categ_id.id
            categ_list = category_obj.search(cr,uid,[('parent_id','=', categ)])
            categ_list.append(categ)
            product_list = product_obj.search(cr,uid,[('categ_id','in', categ_list)])
        else:
            product_list = product_obj.search(cr,uid,[])    
        res = {}
        flag = False
        
        for location in location_ids:
            datas = {}
            res[location] = {}
            empty_list=[]
            move_ids = move_obj.search(cr, uid, [('location_dest_id','=',location),('state','=','done'), ('product_id','in',product_list)], context=context)
            move_ids2 = move_obj.search(cr, uid, [('location_id','=',location),('state','=','done'),('product_id','in',product_list)], context=context)
            
            move_ids.extend(move_ids2)
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                lot_id = move.prodlot_id.id
                if not lot_id:
                    lot_id = 'Empty'
                prod_id = move.product_id.id
                qty = move.product_qty
                datas[(prod_id, lot_id)] = {'product_id': prod_id, 'product_qty':0.0,'location_id': location, 'product_uom': move.product_id.uom_id.id, 'prod_lot_id': lot_id}  
            for data in datas:
                
                val = datas[data]
                lot = val['prod_lot_id']
                if lot == 'Empty':
                    val.update({'prod_lot_id':False})
                product_context.update(uom=val['product_uom'], prodlot_id=val['prod_lot_id'], location=location, from_date=False, to_date=inventory.date, states=['done'], what=['in', 'out'])
                amount = product_obj.get_product_available(cr, uid, [val['product_id']], product_context)[val['product_id']]
                datas[data].update({'product_qty':amount})
                if amount==0.0:
                    empty_list.append(data)
                
            for value in empty_list:
                datas.pop(value)
            if datas:
                flag = True
                res[location] = datas

        if not flag:
            raise osv.except_osv(_('Warning !'), _('No product in this location.'))

        for stock_move in res.values():
            for stock_move_details in stock_move.values():
                stock_move_details.update({'inventory_id': context['active_ids'][0]})
                domain = []
                
                if fill_inventory.set_stock_zero:
                    stock_move_details.update({'product_qty': 0})

                for field, value in stock_move_details.items():
                    domain.append((field, '=', value))

                line_ids = inventory_line_obj.search(cr, uid, domain, context=context)

                if not line_ids:
                    inventory_line_obj.create(cr, uid, stock_move_details, context=context)

        return {'type': 'ir.actions.act_window_close'}
    
    
stock_fill_inventory()