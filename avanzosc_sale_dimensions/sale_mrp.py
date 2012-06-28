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
import netsvc
import time
from tools.translate import _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class sale_order_line(osv.osv):
    
    _inherit="sale.order.line"
    _columns={
              'maker_id': fields.many2one('mrp.maker', 'Config.', readonly=True),
              }

    def copy_data(self, cr, uid, id, default=None, context=None):
            if not default:
                default = {}
            default.update({'maker_id': False})
            return super(sale_order_line, self).copy_data(cr, uid, id, default, context=context)

sale_order_line()
class sale_order(osv.osv):

    _inherit='sale.order'
    
    def _is_configured(self, cr, uid, ids, field_name, arg, context):
        sale_obj = self.pool.get('sale.order')
        product_obj = self.pool.get('product.product')
        sale_line_obj = self.pool.get('sale.order.line')
        
        
        res = {}
        for sale_id in ids:
            product_list = product_obj.search(cr,uid,[('supply_method','=','produce'),('type','in',('product', 'consu'))])
            line_config =sale_line_obj.search(cr,uid,[('order_id','in', ids), ('product_id', 'in', product_list), ('shape', 'in', ('quadrangular', 'cylindrical')),('type','=','make_to_order')])
            if line_config:
                res[sale_id]=False
            else:
                res[sale_id]=True
        return res
    
    
    _columns = {
        'configured': fields.function(_is_configured, method=True, store=False, type="boolean", string='Configured'),        
        'partner_id': fields.many2one('res.partner', 'Customer', readonly=True, states={'draft': [('readonly', False)], 'configure': [('readonly', False)]}, required=True, change_default=True, select=True),
        'order_line': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, states={'draft': [('readonly', False)], 'configure': [('readonly', False)]}),
        'state': fields.selection([
            ('draft', 'Quotation'),
            ('configure', 'Configuration'),
            ('waiting_date', 'Waiting Schedule'),
            ('manual', 'Manual In Progress'),
            ('progress', 'In Progress'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
            ], 'Order State', readonly=True, help="Gives the state of the quotation or sales order. \nThe exception state is automatically set when a cancel operation occurs in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception). \nThe 'Waiting Schedule' state is set when the invoice is confirmed but waiting for the scheduler to run on the date 'Ordered Date'.", select=True),
    }
    
    def action_configure(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'configure'})
        return True
        
    def button_finish(self, cr,uid,ids,context=None):
        
        product_obj = self.pool.get('product.product')
        sale_line_obj = self.pool.get('sale.order.line')

        product_list = product_obj.search(cr,uid,[('supply_method','=','produce'),('type','in',('product', 'consu'))])
        line_config =sale_line_obj.search(cr,uid,[('order_id','in', ids), ('product_id', 'in', product_list), ('shape', 'in', ('quadrangular', 'cylindrical')),('type','=','make_to_order'),('maker_id','=',False)])
        if line_config:
            raise osv.except_osv(_('Error'), _("You have no configured lines."))
        else:
            for sale_id in ids:
                wf_service = netsvc.LocalService("workflow")
                wf_service.trg_validate(uid, 'sale.order', sale_id, 'order_configured', cr) 
        return True
    def configure_lines(self,cr, uid, ids, context=None):
        
        active_list = []
        product_obj = self.pool.get('product.product')
        sale_line_obj = self.pool.get('sale.order.line')

        product_list = product_obj.search(cr,uid,[('supply_method','=','produce'),('type','in',('product', 'consu'))])
        line_config =sale_line_obj.search(cr,uid,[('order_id','in', ids), ('product_id', 'in', product_list), ('shape', 'in', ('quadrangular', 'cylindrical')),('type','=','make_to_order')])
       
        active_list = line_ids
        context.update({'active_ids':active_list})
        if line_ids:
            return {'type': 'ir.actions.act_window',
                    'res_model': 'config.sale.line',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context':context}
        else:
            return {'type':'ir.actions.act_close_window'}
        
    def action_wait(self, cr, uid, ids, *args):
        res = super(sale_order, self).action_wait(cr,uid,ids,*args)
        return res
    
    def action_ship_create(self, cr, uid, ids, *args):
        lot_object = self.pool.get('stock.production.lot')         
        wf_service = netsvc.LocalService("workflow")
        picking_id = False
        move_obj = self.pool.get('stock.move')
        proc_obj = self.pool.get('procurement.order')
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id
        for order in self.browse(cr, uid, ids, context={}):
            proc_ids = []
            output_id = order.shop_id.warehouse_id.lot_output_id.id
            picking_id = False
            for line in order.order_line:
                proc_id = False
                date_planned = datetime.now() + relativedelta(days=line.delay or 0.0)
                date_planned = (date_planned - timedelta(days=company.security_lead)).strftime('%Y-%m-%d %H:%M:%S')
                lote_id = False
                lot_ids = lot_object.search(cr, uid, 
                    [('product_id', '=', line.product_id.id),
                     ('size_x', '=', line.size_x),
                     ('size_y', '=', line.size_y),
                     ('size_z', '=', line.size_z),
                     ('diameter', '=', line.diameter),
                     ('weight', '=', line.weight),                     
                     ('shape', '=', line.shape)])
                if not lot_ids:                
#                    name_seriale = name_serial(line.size_x, line.size_y, line.size_z, line.weight, line.shape, line.diameter)
                    datalote = {
                        'name':' ',
                        'product_id': line.product_id.id,
                        'date' : time.strftime('%Y-%m-%d'),
                        'size_x' : line.size_x,
                        'size_y' : line.size_y,
                        'size_z' :line.size_z,
                        'shape' : line.shape,
                        'diameter' : line.diameter,
                        'density' : line.density,
                        'weight' : line.weight                                                                
                        }
                    lote_id = lot_object.create(cr, uid, datalote)
                    lot_object.generate_serial(cr,uid,[lote_id],*args)
                else:
                    lote_id = lot_ids[0]
                
                
                if line.state == 'done':
                    continue
                move_id = False
                if line.product_id and line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    location_id = order.shop_id.warehouse_id.lot_stock_id.id
                    if not picking_id:
                        pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.out')
                        picking_id = self.pool.get('stock.picking').create(cr, uid, {
                            'name': pick_name,
                            'origin': order.name,
                            'type': 'out',
                            'state': 'auto',
                            'move_type': order.picking_policy,
                            'sale_id': order.id,
                            'address_id': order.partner_shipping_id.id,
                            'note': order.note,
                            'invoice_state': (order.order_policy=='picking' and '2binvoiced') or 'none',
                            'company_id': order.company_id.id,
                        })
                    move_id = self.pool.get('stock.move').create(cr, uid, {
                        'name': line.name[:64],
                        'picking_id': picking_id,
                        'product_id': line.product_id.id,
                        'date': date_planned,
                        'date_expected': date_planned,
                        'product_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': line.product_uos_qty,
                        'product_uos': (line.product_uos and line.product_uos.id)\
                                or line.product_uom.id,
                        'product_packaging': line.product_packaging.id,
                        'address_id': line.address_allotment_id.id or order.partner_shipping_id.id,
                        'location_id': location_id,
                        'location_dest_id': output_id,
                        'sale_line_id': line.id,
                        'tracking_id': False,
                        'prodlot_id':lote_id,
                        'state': 'draft',
                        #'state': 'waiting',
                        'note': line.notes,
                        'company_id': order.company_id.id,
                    })
                bom_id = False
                bom_obj = self.pool.get('mrp.bom')
                bom_id_list = bom_obj.search(cr,uid,[('product_id', '=', line.product_id.id)])
                if bom_id_list:
                    bom_id = bom_id_list[0]
                if line.product_id:
                    proc_id = self.pool.get('procurement.order').create(cr, uid, {
                        'name': line.name,
                        'origin': order.name,
                        'date_planned': date_planned,
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': (line.product_uos and line.product_uos_qty)\
                                or line.product_uom_qty,
                        'product_uos': (line.product_uos and line.product_uos.id)\
                                or line.product_uom.id,
                        'location_id': order.shop_id.warehouse_id.lot_stock_id.id,
                        'procure_method': line.type,
                        'move_id': move_id,
                        'property_ids': [(6, 0, [x.id for x in line.property_ids])],
                        'company_id': order.company_id.id,
                        'size_x':line.size_x,
                        'size_y':line.size_y,
                        'size_z':line.size_z,
                        'shape':line.shape,
                        'diameter':line.diameter,
                        'weight':line.weight,
                        'density':line.density,
                        'price_type':line.sale_price,
                        'maker_id':line.maker_id.id,
                        'bom_id':bom_id,
                    })
                    proc_ids.append(proc_id)
                    self.pool.get('sale.order.line').write(cr, uid, [line.id], {'procurement_id': proc_id})
                    if order.state == 'shipping_except':
                        for pick in order.picking_ids:
                            for move in pick.move_lines:
                                if move.state == 'cancel':
                                    mov_ids = move_obj.search(cr, uid, [('state', '=', 'cancel'),('sale_line_id', '=', line.id),('picking_id', '=', pick.id)])
                                    if mov_ids:
                                        for mov in move_obj.browse(cr, uid, mov_ids):
                                            move_obj.write(cr, uid, [move_id], {'product_qty': mov.product_qty, 'product_uos_qty': mov.product_uos_qty})
                                            proc_obj.write(cr, uid, [proc_id], {'product_qty': mov.product_qty, 'product_uos_qty': mov.product_uos_qty})

       
            val = {}

            if picking_id:
                wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)

            for proc_id in proc_ids:
                wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)

            if order.state == 'shipping_except':
                val['state'] = 'progress'
                val['shipped'] = False

                if (order.order_policy == 'manual'):
                    for line in order.order_line:
                        if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                            val['state'] = 'manual'
                            break
            self.write(cr, uid, [order.id], val)                                     
        return picking_id
sale_order()