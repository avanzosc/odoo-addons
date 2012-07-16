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

from osv import osv, fields

class item_recession(osv.osv_memory):
    _name='item.recession'
    _columns={
              'name':fields.char('Name', size=64),
              }
item_recession()

class item_list(osv.osv_memory):
    _name='item.list'
    _columns = {
                'selected':fields.boolean('Select'),
                'prodlot_id':fields.many2one('stock.production.lot', 'Lot'), 
                'product_id':fields.many2one('product.product', 'Product'), 
                'partner_id':fields.many2one('res.partner', 'Partner'),    
                'recess_id':fields.many2one('item.recession', 'Parent')          
                }
item_list()

class item_recession(osv.osv_memory):
    _inherit='item.recession'
#    _name='item.recession'
    
    _columns={
              'item_ids':fields.one2many('item.list', 'recess_id', 'Item List'),
              }
    def default_get(self, cr, uid, fields, context):
        prodlot_obj = self.pool.get('stock.production.lot')
        
        res = {}
        if 'item_ids' in fields:
            line_list = []
            lot_list = prodlot_obj.search(cr,uid,[('customer','in', context.get('active_ids')),('state', '=', 'inactive'),('is_service','=',False)])
            for lot in lot_list:
                lot_o = prodlot_obj.browse(cr,uid,lot)
                product = lot_o.product_id.id
                partner = lot_o.customer.id
                val = {
                       'selected':True,
                       'prodlot_id':lot,
                       'product_id':product,
                       'partner_id':partner,
                       }
                line_list.append(val)
            res.update({'item_ids': line_list})
        return res
        
    def pick_create(self, cr, uid, ids, context=None):
        
        pick_obj = self.pool.get('stock.picking')
        move_obj= self.pool.get('stock.move')
        partner_obj = self.pool.get('res.partner')
        lot_obj = self.pool.get('stock.production.lot')
        location_obj = self.pool.get('stock.location')
        stock_journal = self.pool.get('stock.journal')
        
        line_ids = context.get('active_ids')
        dest_loca_list = location_obj.search(cr,uid,[('name','=','Recession')])
        stock_journal_list = stock_journal.search(cr,uid,[('name','=','Recession')])
        journal_id = False
        dest_loca = False
        if not dest_loca_list:
            dest_loca = location_obj.create(cr,uid,{'name':'Recession', 'usage':'internal', 'chained_location_type':'none'})
        else:
            dest_loca = dest_loca_list[0]
        if not stock_journal_list:
            journal_id = stock_journal.create(cr,uid,{'name':'Recession'})
        else:
            journal_id = stock_journal_list[0]
        pick_id = pick_obj.create(cr,uid,{'move_type':'one', 'type':'internal', 'stock_journal_id':journal_id})
        for line in self.browse(cr,uid,ids[0]).item_ids:
            if line.selected:
                move_o = move_obj.search(cr,uid,[('prodlot_id', '=',line.prodlot_id.id ),('state','=','done')], order='date')
                move_o.reverse()
                cmove = move_obj.copy(cr,uid,move_o[0])
                cmove_o = move_obj.browse(cr,uid,cmove)
                src_loca = cmove_o.location_dest_id.id
                move_obj.write(cr,uid,[cmove],{'location_id':src_loca, 'location_dest_id':dest_loca, 'picking_id':pick_id, 'is_recession':True})        
        
        return {'type': 'ir.actions.act_window_close'}
        
item_recession()

