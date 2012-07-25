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
import netsvc

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
            lot_list = prodlot_obj.search(cr,uid,[('customer','in', context.get('active_ids')),('is_service','=',False)])
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
        
        
        wf_service = netsvc.LocalService("workflow")
        line_ids = context.get('active_ids')
        dest_loca_list = location_obj.search(cr,uid,[('name','=','Recession')])
        stock_journal_list = stock_journal.search(cr,uid,[('name','=','Recession')])
        journal_id = False
        dest_loca = False
        note = ''
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
            picking_list = pick_obj.search(cr,uid,[('stock_journal_id','=', journal_id),('type','=','internal')])
            move_list = move_obj.search(cr,uid,[('prodlot_id', '=',line.prodlot_id.id ), ('picking_id', 'in', picking_list)])
            if move_list:
                lotname = line.prodlot_id.prefix + '/' + line.prodlot_id.name 
                note = note + "Allready exists recession picking for lot number: %s \n" %(lotname)
            else:
                if line.selected:
                    if line.prodlot_id.state == 'active':
                        wf_service.trg_validate(uid, 'stock.production.lot', line.prodlot_id.id, 'button_inactive', cr)
                    move_o = move_obj.search(cr,uid,[('prodlot_id', '=',line.prodlot_id.id ),('state','=','done')], order='date')
                    if move_o:
                        move_o.reverse()
                        cmove = move_obj.copy(cr,uid,move_o[0])
                        cmove_o = move_obj.browse(cr,uid,cmove)
                        src_loca = cmove_o.location_dest_id.id
                        move_obj.write(cr,uid,[cmove],{'location_id':src_loca, 'location_dest_id':dest_loca, 'picking_id':pick_id, 'is_recession':True})        
                    else:
                        lotname = line.prodlot_id.prefix + '/' + line.prodlot_id.name 
                        note = note + "Stock move not found for lot number: %s \n" %(lotname)
        pick_o = pick_obj.browse(cr,uid,pick_id)
        if not pick_o.move_lines:
            note = note + "\n\nThere is not lot for recession\n\n"
            pick_obj.unlink(cr,uid,[pick_id])
            pick_id = False
        if note == '':
            note=False
        notes_id = self.pool.get('item.notes').create(cr,uid,{'pick_id':pick_id, 'notes':note, 'location_id':dest_loca})
        return { 'type': 'ir.actions.act_window',
                 'res_model': 'item.notes',
                 'view_type': 'form',
                 'view_mode': 'form',
                 'res_id': notes_id,
                 'target': 'new',
                 'context':context}
        
item_recession()
class item_notes(osv.osv_memory):
    _name='item.notes'

    _columns = {
                'pick_id':fields.many2one('stock.picking', 'Picking'),
                'notes':fields.text('Notes'),
                'location_id':fields.many2one('stock.location', 'Dest Location', attrs={'required':[('pick_id', '!=', False)], 'invisible':[('pick_id', '=', False)]})                
                }
    def button_ok(self, cr, uid, ids, context):
        move_obj = self.pool.get('stock.move')
        self_o = self.browse(cr,uid,ids[0])
        pick_id = self_o.pick_id
        location_id = self_o.location_id.id
        if pick_id:
            for line in pick_id.move_lines:
                move_obj.write(cr,uid,line.id, {'location_dest_id':location_id})
            return { 'type': 'ir.actions.act_window',
                         'res_model': 'stock.picking',
                         'view_type': 'form',
                         'view_mode': 'form',
                         'res_id': pick_id.id,
                         'target': 'new',
                         'context':context}
        else:
            return {'type': 'ir.actions.act_window_close'}
item_notes()
