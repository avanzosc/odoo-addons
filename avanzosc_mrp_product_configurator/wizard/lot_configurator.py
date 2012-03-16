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
import netsvc

class mrp_lot_configurator_list(osv.osv_memory):

    _name = 'mrp.lot.configurator.list'
    _description = 'Lot Configurator List'
 
    _columns = {
            'name': fields.char('Name', size=64),
            'product_id': fields.many2one('product.product', 'Product'),
            'prodlot_id': fields.many2one('stock.production.lot', 'MAC Address / Serial Nº', required=True),
            'cofig_id': fields.many2one('mrp.bom.configurator', 'Configurator'),
    }
    
mrp_lot_configurator_list()

class mrp_lot_configurator(osv.osv_memory):

    _name = 'mrp.lot.configurator'
    _description = 'Lot Configurator List'
 
    _columns = {
            'fin_prod': fields.many2one('product.product', 'Finished Product', readonly=True),
            'fin_prodlot': fields.many2one('stock.production.lot', 'MAC Address', required=True),
            'installer_id': fields.many2one('res.partner', 'Installer', readonly=True, required=True),
            'technician_id': fields.many2one('res.partner.contact', 'Technician', required=True),
            'customer_id': fields.many2one('res.partner', 'Customer', readonly=True, required=True),
            'customer_addr_id': fields.many2one('res.partner.address', 'Customer Address', readonly=True, required=True),
            'customer_loc_id': fields.many2one('stock.location', 'Customer Location'),
            'agreement': fields.many2one('inv.agreement', 'Agreement'),
            'config_ids': fields.one2many('mrp.lot.configurator.list', 'cofig_id', 'Configurator'),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        option_obj = self.pool.get('mrp.bom.product.list')
        if context is None:
            context = {}
        order_obj = self.pool.get('mrp.production')
        sale_obj = self.pool.get('sale.order')
        move_obj = self.pool.get('stock.move')
        res = {}
        values = {}
        prods = []
        prods_fin = []
        agreement = False
        if context['active_model'] != 'mrp.production':
            for sale in sale_obj.browse(cr, uid, context['active_ids']):
                id = (order_obj.search(cr, uid, [('origin', '=', sale.name), ('state', 'in', ('confirmed','ready'))]))
                if sale.agreement:
                    agreement = sale.agreement.id
        else:
            id = context['active_ids']
        for order in order_obj.browse(cr, uid, id):
            for move in order.move_lines:
                if move.product_id.track_production:
                    if move.product_id.code:
                        values = {
                            'name': '[' + move.product_id.code + '] ' + move.product_id.name,
                            'product_id': move.product_id.id
                        }
                    else:
                        values = {
                            'name': move.product_id.name,
                            'product_id': move.product_id.id
                        }
                    prods.append(values)
            if not prods:
                raise osv.except_osv(_('User Error'), _('Trazable products not found !'))
            for move in order.move_created_ids:
                prods_fin.append(move)    
            res = {
                'agreement': agreement,
                'fin_prod': prods_fin[0].product_id.id,
                'installer_id': context.get('installer_id'),
                'technician_id': context.get('technician_id'),
                'customer_id': context.get('customer_id'),
                'customer_addr_id': context.get('customer_addr_id'),
                'customer_loc_id': context.get('customer_loc_id'),
                'config_ids': prods,
            }
            break
        return res
    
    def set_lots(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        if context is None:
            context = {}
        order_obj = self.pool.get('mrp.production')
        prodlot_obj = self.pool.get('stock.production.lot')
        picking_obj = self.pool.get('stock.picking')
        sale_obj = self.pool.get('sale.order')
        move_obj = self.pool.get('stock.move')
        config = self.browse(cr, uid, ids)[0]
        sale_ids = False
        if context['active_model'] != 'mrp.production':
            sale_ids = context['active_ids']
            for sale in sale_obj.browse(cr, uid, sale_ids):
                id = (order_obj.search(cr, uid, [('origin', '=', sale.name), ('state', 'in', ('confirmed','ready'))]))
        else:
            id = context['active_ids']
        if id:
            for order in order_obj.browse(cr, uid, id):
                values = {
                    'installer': config.installer_id.id,
                    'technician': config.technician_id.id,
                    'customer': config.customer_id.id,
                    'cust_address': config.customer_addr_id.id,
                }
                for move in order.move_lines:
                    for list in config.config_ids:
                        if list.prodlot_id.product_id.id == move.product_id.id:
                            values.update({
                                'agreement': config.agreement.id,
                            })
                            prodlot_obj.write(cr, uid, [list.prodlot_id.id], values)
                            move_obj.write(cr, uid, [move.id], {'prodlot_id': list.prodlot_id.id, 'location_dest_id': config.customer_loc_id.id})
                            wf_service.trg_validate(uid, 'stock.production.lot', list.prodlot_id.id, 'button_active', cr)
                        else:
                            move_obj.write(cr, uid, [move.id], {'location_dest_id': config.customer_loc_id.id})
                if config.agreement:
                    values.update({
                        'agreement': config.agreement.id,
                        'production_id': order.id,
                        'is_service': True,
                    })
                for move in order.move_created_ids:
                    prodlot_obj.write(cr, uid, config.fin_prodlot.id, values)
                    move_obj.write(cr, uid, [move.id], {'prodlot_id': config.fin_prodlot.id})
#                    MUGIMENDUEI LOTEA EZARRI ALBARANEAN
#                    picking_obj.write(cr, uid, picking_obj.search(cr, uid, [('production_id', '=', order.id)]), {'prodlot_id': config.fin_prodlot.id})
                    wf_service.trg_validate(uid, 'stock.production.lot', config.fin_prodlot.id, 'button_active', cr)
                if order.state == 'confirmed':
                    order_obj.force_production(cr, uid, [order.id])
                wf_service.trg_validate(uid, 'mrp.production', order.id, 'button_produce', cr)
                wf_service.trg_validate(uid, 'mrp.production', order.id, 'button_produce_done', cr)
                context.update({
                    'active_model': 'mrp.production',
                    'active_ids': [order.id],
                    'active_id': order.id,
                })
                order_obj.action_produce(cr, uid, order.id, order.product_qty, 'consume_produce', context=context)
                break
            if sale_ids:
                for sale in sale_obj.browse(cr, uid, sale_ids):
                    id = (order_obj.search(cr, uid, [('origin', '=', sale.name), ('state', 'in', ('confirmed','ready'))]))
                    context.update({
                            'active_model': 'sale.order',
                            'active_ids': [sale.id],
                            'active_id': sale.id,
                        })
                if id:
                    wizard = {
                            'type': 'ir.actions.act_window',
                            'res_model': 'mrp.lot.configurator',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'target': 'new',
                            'context':context
                        }
                    return wizard
                else:
                    pick_ids = []
                    #HEMEN ALBARANAREN LOGIKA IDATZI BEHAR DA
                    for sale in sale_obj.browse(cr, uid, sale_ids):
                        for pick in sale.picking_ids:
                            pick_ids.append(pick.id)
                        picking_obj.unlink(cr, uid, pick_ids)
                        wf_service.trg_validate(uid, 'sale.order', sale.id, 'ship_corrected', cr)
        return {'type': 'ir.actions.act_window_close'}
    
mrp_lot_configurator()