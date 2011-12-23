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
from osv import fields,osv
import decimal_precision as dp
import time, datetime
import netsvc
from tools.translate import _

class mrp_production(osv.osv):
    _inherit = 'mrp.production'
    
    _columns = {
        'real_date':fields.datetime('Real Date', help="Real Date of Completion"),
    }
    
    _defaults = {
        'real_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
mrp_production()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    
    _columns = {
        'real_date':fields.datetime('Real Date', help="Real Date of Completion"),
    }
    
    _defaults = {
        'real_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
stock_picking()
    
class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    _columns = {
        'inventory_ids':fields.many2many('stock.inventory', 'stock_inventory_move_rel','move_id', 'inventory_id', 'Inventories'),
        'production_ids': fields.many2many('mrp.production', 'mrp_production_move_ids', 'move_id', 'production_id', 'Consumed Products'),
    }
    
    def action_done(self, cr, uid, ids, context=None):
        """ Makes the move done and if all moves are done, it will finish the picking.
        @return:
        """
        partial_datas=''
        picking_ids = []
        move_ids = []
        partial_obj=self.pool.get('stock.partial.picking')
        wf_service = netsvc.LocalService("workflow")
        partial_id=partial_obj.search(cr,uid,[])
        if partial_id:
            partial_datas = partial_obj.read(cr, uid, partial_id, context=context)[0]
        if context is None:
            context = {}

        todo = []
        for move in self.browse(cr, uid, ids, context=context):
            if move.state=="draft":
                todo.append(move.id)
        if todo:
            self.action_confirm(cr, uid, todo, context=context)
            todo = []

        for move in self.browse(cr, uid, ids, context=context):
            if move.state in ['done','cancel']:
                continue
            move_ids.append(move.id)
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            if move.inventory_ids:
                for inventory in move.inventory_ids:
                    date = self.pool.get('stock.inventory').browse(cr, uid, inventory.id).date
            if move.production_id:
                date = self.pool.get('mrp.production').browse(cr, uid, move.production_id.id).real_date
            if move.production_ids:
                for production in move.production_ids:
                    date = self.pool.get('mrp.production').browse(cr, uid, production.id).real_date
            if move.picking_id:
                picking_ids.append(move.picking_id.id)
                date = self.pool.get('stock.picking').browse(cr, uid, move.picking_id.id).real_date
            if move.move_dest_id.id and (move.state != 'done'):
                self.write(cr, uid, [move.id], {'move_history_ids': [(4, move.move_dest_id.id)]})
                #cr.execute('insert into stock_move_history_ids (parent_id,child_id) values (%s,%s)', (move.id, move.move_dest_id.id))
                if move.move_dest_id.state in ('waiting', 'confirmed'):
                    if move.prodlot_id.id and move.product_id.id == move.move_dest_id.product_id.id:
                        self.write(cr, uid, [move.move_dest_id.id], {'prodlot_id':move.prodlot_id.id})
                    self.force_assign(cr, uid, [move.move_dest_id.id], context=context)
                    if move.move_dest_id.picking_id:
                        wf_service.trg_write(uid, 'stock.picking', move.move_dest_id.picking_id.id, cr)
                    if move.move_dest_id.auto_validate:
                        self.action_done(cr, uid, [move.move_dest_id.id], context=context)

            self._create_product_valuation_moves(cr, uid, move, context=context)
            prodlot_id = partial_datas and partial_datas.get('move%s_prodlot_id' % (move.id), False)
            if prodlot_id:
                self.write(cr, uid, [move.id], {'prodlot_id': prodlot_id}, context=context)
            if move.state not in ('confirmed','done','assigned'):
#                todo.append(move.id)
                self.action_confirm(cr, uid, [move.id], context=context)
                
            self.write(cr, uid, [move.id], {'state': 'done', 'date': date}, context=context)
#        if todo:
#            self.action_confirm(cr, uid, todo, context=context)
#
#        self.write(cr, uid, move_ids, {'state': 'done', 'date': time.strftime('%Y-%m-%d %H:%M:%S')}, context=context)
        for id in move_ids:
             wf_service.trg_trigger(uid, 'stock.move', id, cr)

        for pick_id in picking_ids:
            wf_service.trg_write(uid, 'stock.picking', pick_id, cr)

        return True
stock_move()