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

class mrp_bom_product_list(osv.osv_memory):

    _name = 'mrp.bom.product.list'
    _description = 'BOM Configurator Product List'
 
    _columns = {
            'name': fields.char('Name', size=64),
            'product_id': fields.many2one('product.product', 'Product'),
            'checked': fields.boolean('Checked'),
            'cofig_id': fields.many2one('mrp.bom.configurator', 'Configurator'),
    }
    
mrp_bom_product_list()

class mrp_bom_product_list_one(osv.osv_memory):

    _name = 'mrp.bom.product.list.one'
    _description = 'BOM Configurator Product List'
 
    _columns = {
            'name': fields.char('Name', size=64),
            'product_id': fields.many2one('product.product', 'Product'),
            'cofig_one_id': fields.many2one('mrp.bom.configurator', 'Configurator'),
    }
    
mrp_bom_product_list_one()

class mrp_bom_configurator(osv.osv_memory):

    _name = 'mrp.bom.configurator'
    _description = 'BOM Configurator'
 
    _columns = {
            'mrp_production': fields.many2one('mrp.production', 'Production Order', readonly=True, required=True),
            'type': fields.selection([
                ('one','One'),
                ('multiple','Multiple')], 'Select'),
            'product_id': fields.many2one('product.product', 'Replace Product', readonly=True),
            'product_list':fields.one2many('mrp.bom.product.list', 'cofig_id','Product List for multiple selection'),
            'installer_id': fields.many2one('res.partner', 'Installer', readonly=True, required=True),
            'technician_id': fields.many2one('res.partner.contact', 'Technician', required=True),
            'customer_id': fields.many2one('res.partner', 'Customer', readonly=True, required=True),
            'customer_addr_id': fields.many2one('res.partner.address', 'Customer Address', readonly=True, required=True),
            'customer_loc_id': fields.many2one('stock.location', 'Customer location'),
    }
            
    def default_get(self, cr, uid, fields, context=None):
        option_obj = self.pool.get('mrp.bom.product.list')
        if context is None:
            context = {}
        order_obj = self.pool.get('mrp.production')
        sale_obj = self.pool.get('sale.order')
        res = {}
        values = {}
        items = []
        if context['active_model'] != 'mrp.production':
            for sale in sale_obj.browse(cr, uid, context['active_ids']):
                id = (order_obj.search(cr, uid, [('origin', '=', sale.name), ('state', '=', 'configure')]))
        else:
            id = context['active_ids']
        for order in order_obj.browse(cr, uid, id):
            if order.state == 'configure':
                items = []
                for line in order.product_lines:
                    res = {
                        'product_id': False,
                        'type': False,
                    }
                    if line.product_id.alt_product_ids:
                        res = {
                            'product_id': line.product_id.id,
                            'type': line.product_id.selection_type,
                        }
                        for item in line.product_id.alt_product_ids:
                            if item.code:
                                values = {
                                    'name': '[' + item.code + '] ' + item.name,
                                    'product_id':item.id,
                                }
                            else:
                                values = {
                                    'name': item.name,
                                    'product_id':item.id,
                                }
                            items.append(values)
                        break
            res.update({
                'mrp_production': order.id,
                'product_list': items,
                'installer_id': context.get('installer_id'),
                'technician_id': context.get('technician_id'),
                'customer_id': context.get('customer_id'),
                'customer_addr_id': context.get('customer_addr_id'),
            })
            return res
        return res
    
    def next(self, cr, uid, ids, context=None):
        wizard = {}
        wf_service = netsvc.LocalService("workflow")
        order_obj = self.pool.get('mrp.production')
        sale_obj = self.pool.get('sale.order')
        order_id = False
        for conf in self.browse(cr, uid, ids):
            if not order_obj.test_replacement(cr, uid, [conf.mrp_production.id], context):
                    wf_service.trg_validate(uid, 'mrp.production', conf.mrp_production.id, 'button_configure', cr)
                    
            if context['active_model'] != 'mrp.production':
                for sale in sale_obj.browse(cr, uid, context['active_ids']):
                    order_id = order_obj.search(cr, uid, [('origin', '=', sale.name), ('state', '=', 'configure')])
                
            if order_id:
                context.update({
                    'installer_id': context.get('installer_id'),
                    'technician_id': context.get('technician_id'),
                    'customer_id': context.get('customer_id'),
                    'customer_addr_id': context.get('customer_addr_id'),
                    'customer_loc_id': context.get('customer_loc_id'),
                })
                wizard = {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mrp.bom.configurator',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context':context
                }
            else:
                context.update({
                    'installer_id': context.get('installer_id'),
                    'technician_id': context.get('technician_id'),
                    'customer_id': context.get('customer_id'),
                    'customer_addr_id': context.get('customer_addr_id'),
                    'customer_loc_id': context.get('customer_loc_id'),
                })
                wizard = {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mrp.lot.configurator',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context':context
                }
        return wizard 
    
    def product_replacement(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        order_obj = self.pool.get('mrp.production')
        order_line = self.pool.get('mrp.production.product.line')
        sale_obj = self.pool.get('sale.order')
        order_id = []
        items = []
        if context is None:
            context = {}
        
        for conf in self.browse(cr, uid, ids):
            for alt_prod in conf.product_list:
                if alt_prod.checked:
                    items.append(alt_prod)
            if conf.type == 'one':
                    if len(items) == 1:
                        alt_id = order_line.search(cr, uid, [('product_id', '=', conf.product_id.id), ('production_id', '=', conf.mrp_production.id)])
                        order_line.write(cr, uid, alt_id, {'product_id': items[0].product_id.id})
                    else:
                        raise osv.except_osv(_('User error'), _('Select only one product, please !'))
            else:
                for item in items:
                    alt_id = order_line.search(cr, uid, [('product_id', '=', conf.product_id.id), ('production_id', '=', conf.mrp_production.id)])
                    if alt_id:
                        order_line.write(cr, uid, alt_id, {'product_id': item.product_id.id})
                    else:
                        order_line.create(cr, uid, {'product_id': item.product_id.id,
                                                    'name': item.product_id.name,
                                                    'product_uom': item.product_id.uom_id.id,
                                                    'product_qty': 1,
                                                    'production_id': conf.mrp_production.id,
                                                    })
                        
            if not order_obj.test_replacement(cr, uid, [conf.mrp_production.id], context):
                wf_service.trg_validate(uid, 'mrp.production', conf.mrp_production.id, 'button_configure', cr)
                
            if context['active_model'] != 'mrp.production':
                for sale in sale_obj.browse(cr, uid, context['active_ids']):
                    order_id = order_obj.search(cr, uid, [('origin', '=', sale.name), ('state', '=', 'configure')])
                
            if order_id:
                context.update({
                    'installer_id': context.get('installer_id'),
                    'technician_id': context.get('technician_id'),
                    'customer_id': context.get('customer_id'),
                    'customer_addr_id': context.get('customer_addr_id'),
                    'customer_loc_id': context.get('customer_loc_id'),
                })
                wizard = {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mrp.bom.configurator',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context':context
                }
                return wizard
            else:
                context.update({
                    'installer_id': context.get('installer_id'),
                    'technician_id': context.get('technician_id'),
                    'customer_id': context.get('customer_id'),
                    'customer_addr_id': context.get('customer_addr_id'),
                    'customer_loc_id': context.get('customer_loc_id'),
                })
                wizard = {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mrp.lot.configurator',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context':context
                }
                return wizard
        return {'type': 'ir.actions.act_window_close'}
    
mrp_bom_configurator()