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
from osv import osv
from osv import fields
from tools.translate import _
import netsvc
class set_lot2move(osv.osv_memory):
    
    _name="set.lot2move"
    
    
    def button_ok(self, cr, uid, ids, context={}):
        wf_service = netsvc.LocalService("workflow")
        production_obj = self.pool.get('mrp.production')
        lot_obj = self.pool.get('stock.production.lot')
        move_obj = self.pool.get('stock.move')
        
        mrp_ids = context.get('active_ids')
        
        for mrp_o in production_obj.browse(cr,uid,mrp_ids):
            if mrp_o.state == 'done' and mrp_o.move_created_ids2:
                final_lot = mrp_o.move_created_ids2[0].prodlot_id
                prefix = final_lot.prefix
                lot_name = final_lot.name
                for move in mrp_o.move_lines2:
                    if move.prodlot_id and move.prodlot_id.prefix!=prefix:
                        lot_id = False
                        print move.product_id
                        lot_list = lot_obj.search(cr,uid,[('product_id','=',move.product_id.id),('prefix','=',prefix),('name', '=', lot_name),('state','=','nouse'), ('is_service','=',False)])
                        
                        if not lot_list:
                            lot_id = lot_obj.create(cr,uid,{'product_id':move.product_id.id, 'prefix':prefix, 'name':lot_name, 'state':'nouse', 'agreement':final_lot.agreement.id, 'is_service':False})
                        else:
                            lot_id = lot_list[0]
                            lot_obj.write(cr,uid,[lot_id], {'agreement':final_lot.agreement.id})
                        lot_o = lot_obj.browse(cr,uid,lot_id)
                        print lot_o.product_id
                        print move.product_id
                        move_obj.write(cr,uid,[move.id],{'prodlot_id':lot_id})
                        wf_service.trg_validate(uid, 'stock.production.lot', lot_id, 'button_active', cr)
        return {'type': 'ir.actions.act_window_close'}
set_lot2move()