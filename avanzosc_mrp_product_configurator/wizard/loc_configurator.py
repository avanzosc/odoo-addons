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

class mrp_loc_configurator(osv.osv_memory):

    _name = 'mrp.loc.configurator'
    _description = 'Loc Configurator'
    
    def view_init(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        order_obj = self.pool.get('mrp.production')
        sale_obj = self.pool.get('sale.order')
        if context['active_model'] != 'mrp.production':
            for sale in sale_obj.browse(cr, uid, context['active_ids']):
                id = (order_obj.search(cr, uid, [('origin', '=', sale.name)]))
        else:
            id = context['active_ids']
        if not id:
            raise osv.except_osv(_('Error'), _('Cannot found MRP order to configure !'))
        for order in order_obj.browse(cr, uid, id):
            if order.state == 'done':
                raise osv.except_osv(_('User error'), _('The order is already configured !'))
 
    _columns = {
            'installer_loc_id': fields.many2one('stock.location', 'Installer Location', domain=[('usage', '=', 'internal')], required=True),
            'customer_loc_id': fields.many2one('stock.location', 'Customer Location', domain=[('usage', '=', 'internal')], required=True),
            'installer_id': fields.many2one('res.partner', 'Installer', readonly=True, required=True),
            'technician_id': fields.many2one('res.partner.contact', 'Technician', required=True),
            'customer_id': fields.many2one('res.partner', 'Customer', readonly=True, required=True),
            'customer_addr_id': fields.many2one('res.partner.address', 'Customer Address', readonly=True, required=True),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        order_obj = self.pool.get('mrp.production')
        sale_obj = self.pool.get('sale.order')
        res = {}
        if context['active_model'] == 'mrp.production':
            raise osv.except_osv(_('User error'), _('This wizard cannot be executed from MRP view !'))
        else:
            id = context['active_ids']
            for sale in sale_obj.browse(cr, uid, context['active_ids']):
                ids = (order_obj.search(cr, uid, [('origin', '=', sale.name)]))
        if not ids:
            raise osv.except_osv(_('Error'), _('Cannot found MRP order to configure !'))
        for order in sale_obj.browse(cr, uid, id):
            res = {
                'customer_id': order.partner_id.id,
                'customer_addr_id': order.partner_shipping_id.id,
            }
        return res
    
    def onchange_installer(self, cr, uid, ids, installer_loc_id, context=None):
        res ={}
        installer = self.pool.get('stock.location').browse(cr, uid, installer_loc_id)
        if installer.address_id:
            partner_ids = self.pool.get('res.partner').search(cr, uid, [('address', '=', installer.address_id.id)])
            for partner_id in partner_ids:
                res = {
                    'installer_id': partner_id,
                }
        else:
            raise osv.except_osv(_('User Error'), _('This location hasn\'t got any address !'))
        return {'value': res}
    
    def set_locations(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        order_obj = self.pool.get('mrp.production')
        sale_obj = self.pool.get('sale.order')
        if context['active_model'] != 'mrp.production':
            for sale in sale_obj.browse(cr, uid, context['active_ids']):
                id = (order_obj.search(cr, uid, [('origin', '=', sale.name)]))
        else:
            id = context['active_ids']
        for conf in self.browse(cr, uid, ids):
            installer = self.pool.get('stock.location').browse(cr, uid, conf.installer_loc_id.id)
            installer_id = self.pool.get('res.partner').search(cr, uid, [('address', '=', installer.address_id.id)])[0]
            for order in order_obj.browse(cr, uid, id):
                order_obj.write(cr, uid, order.id, {'location_src_id': conf.installer_loc_id.id, 'location_dest_id': conf.customer_loc_id.id})
            context.update({
                    'installer_id': installer_id, 
                    'technician_id': conf.technician_id.id, 
                    'customer_id': conf.customer_id.id,
                    'customer_addr_id': conf.customer_addr_id.id,
                    'customer_loc_id': conf.customer_loc_id.id,
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
        return {'type': 'ir.actions.act_window_close'}
    
mrp_loc_configurator()