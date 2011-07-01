# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc, OpenERP Professional Services   
#    Copyright (C) 2010-2011 Avanzosc S.L (http://www.avanzosc.com). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

import netsvc
from datetime import datetime
from tools.translate import _

from osv import osv
from osv import fields


class mrp_production(osv.osv):

    _inherit = 'mrp.production'
    
    _columns = {
        'qty_per_lot': fields.float('Qty per Lot', states={'draft':[('readonly',False)]}),
    }
    
    def onchange_product_qty(self, cr, uid, ids, qty, context=None):
        res = {}
        if qty:
            res = {
                'qty_per_lot': qty
            }
        return {'value': res}
    
    def create_lot(self, cr, uid, ids, product_id, context=None):
        product = self.pool.get('product.product').browse(cr, uid, product_id)
        name = self.pool.get('ir.sequence').get(cr, uid, product.lot_sequence.code)
        data = {
            'name': name,
            'product_id': product.id,
        }
        return self.pool.get('stock.production.lot').create(cr, uid, data)
 
    def get_lot(self, cr, uid, product_id, location_id, qty, context=None):
        lot_obj = self.pool.get('stock.production.lot')
        move_obj = self.pool.get('stock.move')
        product = self.pool.get('product.product').browse(cr, uid, product_id)
        lot_list = {}
        res = []
        
        inventory_obj = self.pool.get('report.stock.inventory')
        ids = inventory_obj.search(cr, uid, [('product_id', '=', product_id), ('location_id', '=', location_id)])
        for inventory in inventory_obj.browse(cr, uid, ids):
            if inventory.prodlot_id and inventory.state == 'done':
                if str(inventory.prodlot_id.id) in lot_list:
                    lot_list[str(inventory.prodlot_id.id)] += inventory.product_qty
                else:
                    lot_list.update({str(inventory.prodlot_id.id): inventory.product_qty})
       
        if not lot_list:
            if product.track_production:
                raise osv.except_osv(_('Stock error'), _('%s needs production lots ! \
                            \nNo lot founded for this product!') % (product.name))
            return False
        
        for lot_id in lot_list.keys():
            if lot_list[lot_id] == 0:
                del lot_list[lot_id]
       
        while qty > 0:
            cur_lot = 0
            if not lot_list and qty > 0:
                raise osv.except_osv(_('Stock error'), _('There is no enough stock for %s ! \
                            \n%s KG(s) missing!') % (product.name, round(qty,3)))
            elif product.lot_type == 'lifo':
                cur_lot = self.lifo_lot(cr, uid, lot_list, qty, context)
            elif product.lot_type == 'fifo':
                cur_lot = self.fifo_lot(cr, uid, lot_list, qty, context)
                
            if lot_list[cur_lot] <= qty:
                qty -= lot_list[cur_lot]
                res.append({cur_lot: lot_list[cur_lot]})
                del lot_list[cur_lot]
            else:
                res.append({cur_lot: qty})
                qty = 0
        
        return res
    
    def fifo_lot(self, cr, uid, lot_list, qty, context):
        lot_obj = self.pool.get('stock.production.lot')
        fifo_lot = False
        for lot_id in lot_list.keys():
            cur_lot = lot_obj.browse(cr, uid, int(lot_id))
            if not fifo_lot and (lot_list[lot_id] > 0):
                fifo_lot = cur_lot
            elif fifo_lot and cur_lot.date < fifo_lot.date and (lot_list[lot_id] > 0):
                fifo_lot = cur_lot
        return str(fifo_lot.id)
    
    def lifo_lot(self, cr, uid, lot_list, qty, context):
        lot_obj = self.pool.get('stock.production.lot')
        lifo_lot = False
        for lot_id in lot_list.keys():
            cur_lot = lot_obj.browse(cr, uid, int(lot_id))
            if not lifo_lot and (lot_list[lot_id] > 0):
                lifo_lot = cur_lot
            elif lifo_lot and cur_lot.date > lifo_lot.date and (lot_list[lot_id] > 0):
                lifo_lot = cur_lot
        return str(lifo_lot.id)
    
    def action_confirm(self, cr, uid, ids):
        """ Confirms production order.
        @return: Newly generated picking Id.
        """
        picking_id = False
        proc_ids = []
        res_final_id = []
        seq_obj = self.pool.get('ir.sequence')
        pick_obj = self.pool.get('stock.picking')
        move_obj = self.pool.get('stock.move')
        proc_obj = self.pool.get('procurement.order')
        wf_service = netsvc.LocalService("workflow")
        for production in self.browse(cr, uid, ids):
            if not production.product_lines:
                self.action_compute(cr, uid, [production.id])
                production = self.browse(cr, uid, [production.id])[0]
            routing_loc = None
            pick_type = 'internal'
            address_id = False
            if production.bom_id.routing_id and production.bom_id.routing_id.location_id:
                routing_loc = production.bom_id.routing_id.location_id
                if routing_loc.usage <> 'internal':
                    pick_type = 'out'
                address_id = routing_loc.address_id and routing_loc.address_id.id or False
                routing_loc = routing_loc.id
            pick_name = seq_obj.get(cr, uid, 'stock.picking.' + pick_type)
            picking_id = pick_obj.create(cr, uid, {
                'name': pick_name,
                'origin': (production.origin or '').split(':')[0] + ':' + production.name,
                'type': pick_type,
                'move_type': 'one',
                'state': 'auto',
                'address_id': address_id,
                'auto_picking': self._get_auto_picking(cr, uid, production),
                'company_id': production.company_id.id,
            })

            source = production.product_id.product_tmpl_id.property_stock_production.id
            if production.product_id.track_production:
                qty = production.product_qty/production.qty_per_lot
                while qty != 0:
                    final_lot = self.create_lot(cr, uid, ids, production.product_id.id)
                    data = {
                        'name':'PROD:' + production.name,
                        'date': production.date_planned,
                        'product_id': production.product_id.id,
                        'product_qty': production.qty_per_lot,
                        'product_uom': production.product_uom.id,
                        'prodlot_id': final_lot,
                        'product_uos_qty': production.product_uos and production.product_uos_qty or False,
                        'product_uos': production.product_uos and production.product_uos.id or False,
                        'location_id': source,
                        'location_dest_id': production.location_dest_id.id,
                        'move_dest_id': production.move_prod_id.id,
                        'state': 'waiting',
                        'company_id': production.company_id.id,
                    }
                    res_final_id.append(move_obj.create(cr, uid, data))
                    qty -= 1
            else:
                data = {
                    'name':'PROD:' + production.name,
                    'date': production.date_planned,
                    'product_id': production.product_id.id,
                    'product_qty': production.product_qty,
                    'product_uom': production.product_uom.id,
                    'product_uos_qty': production.product_uos and production.product_uos_qty or False,
                    'product_uos': production.product_uos and production.product_uos.id or False,
                    'location_id': source,
                    'location_dest_id': production.location_dest_id.id,
                    'move_dest_id': production.move_prod_id.id,
                    'state': 'waiting',
                    'company_id': production.company_id.id,
                }
                res_final_id.append(move_obj.create(cr, uid, data))
            self.write(cr, uid, [production.id], {'move_created_ids': [(6, 0, res_final_id)]})
            moves = []
            for line in production.product_lines:
                move_id = False
                newdate = production.date_planned
                if line.product_id.type in ('product', 'consu'):
                    if line.product_id.lot_type != 'manual':
                        lot_list = self.get_lot(cr, uid, line.product_id.id, production.location_src_id.id, line.product_qty)
                        for lot_id in lot_list:
                            value_dest = {
                                'name':'PROD:' + production.name,
                                'date': production.date_planned,
                                'product_id': line.product_id.id,
                                'product_qty': lot_id.values()[0],
                                'product_uom': line.product_uom.id,
                                'product_uos_qty': line.product_uos and line.product_uos_qty or False,
                                'product_uos': line.product_uos and line.product_uos.id or False,
                                'location_id': routing_loc or production.location_src_id.id,
                                'location_dest_id': source,
                                #'move_dest_id': res_final_id,
                                'state': 'waiting',
                                'company_id': production.company_id.id,
                            }
                            if lot_id:
                                value_dest.update({'prodlot_id': lot_id.keys()[0]})
                            res_dest_id = move_obj.create(cr, uid, value_dest)
                            moves.append(res_dest_id)
                            value_move = {
                                'name':'PROD:' + production.name,
                                'picking_id':picking_id,
                                'product_id': line.product_id.id,
                                'product_qty': lot_id.values()[0],
                                'product_uom': line.product_uom.id,
                                'product_uos_qty': line.product_uos and line.product_uos_qty or False,
                                'product_uos': line.product_uos and line.product_uos.id or False,
                                'date': newdate,
                                'move_dest_id': res_dest_id,
                                'location_id': production.location_src_id.id,
                                'location_dest_id': routing_loc or production.location_src_id.id,
                                #'state': 'waiting',
                                'company_id': production.company_id.id,
                            }
                            if lot_id:
                                value_move.update({'prodlot_id': lot_id.keys()[0]})
                            move_id = move_obj.create(cr, uid, value_move)
                    else:
                        value_dest = {
                            'name':'PROD:' + production.name,
                            'date': production.date_planned,
                            'product_id': line.product_id.id,
                            'product_qty': line.product_qty,
                            'product_uom': line.product_uom.id,
                            'product_uos_qty': line.product_uos and line.product_uos_qty or False,
                            'product_uos': line.product_uos and line.product_uos.id or False,
                            'location_id': routing_loc or production.location_src_id.id,
                            'location_dest_id': source,
                            #'move_dest_id': res_final_id,
                            'state': 'waiting',
                            'company_id': production.company_id.id,
                        }
                        res_dest_id = move_obj.create(cr, uid, value_dest)
                        moves.append(res_dest_id)
                        value_move = {
                            'name':'PROD:' + production.name,
                            'picking_id':picking_id,
                            'product_id': line.product_id.id,
                            'product_qty': line.product_qty,
                            'product_uom': line.product_uom.id,
                            'product_uos_qty': line.product_uos and line.product_uos_qty or False,
                            'product_uos': line.product_uos and line.product_uos.id or False,
                            'date': newdate,
                            'move_dest_id': res_dest_id,
                            'location_id': production.location_src_id.id,
                            'location_dest_id': routing_loc or production.location_src_id.id,
                            #'state': 'waiting',
                            'company_id': production.company_id.id,
                        }
                        move_id = move_obj.create(cr, uid, value_move)
                proc_id = proc_obj.create(cr, uid, {
                    'name': (production.origin or '').split(':')[0] + ':' + production.name,
                    'origin': (production.origin or '').split(':')[0] + ':' + production.name,
                    'date_planned': newdate,
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    'product_uom': line.product_uom.id,
                    'product_uos_qty': line.product_uos and line.product_qty or False,
                    'product_uos': line.product_uos and line.product_uos.id or False,
                    'location_id': production.location_src_id.id,
                    'procure_method': line.product_id.procure_method,
                    'move_id': move_id,
                    'company_id': production.company_id.id,
                })
                wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)
                proc_ids.append(proc_id)
            wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
            self.write(cr, uid, [production.id], {'picking_id': picking_id, 'move_lines': [(6,0,moves)], 'state':'confirmed'})
            message = _("Manufacturing order '%s' is scheduled for the %s.") % (
                production.name,
                datetime.strptime(production.date_planned,'%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'),
            )
            self.log(cr, uid, production.id, message)
        return picking_id
    
mrp_production()