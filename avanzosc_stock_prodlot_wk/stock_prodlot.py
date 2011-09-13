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

class stock_production_lot(osv.osv):

    _inherit='stock.production.lot'
 
    _columns = {
            'name': fields.char('Serial Nº', size=64, required=True, help="Unique mac address"),
            'prefix': fields.char('MAC Address', size=64, help="Optional serial number"),
            'state_history': fields.one2many('stock.prodlot.history', 'prodlot_id', 'History'),
            'installer': fields.many2one('res.partner', 'Installer', domain=[('installer', '=', True)]),
            'technician': fields.many2one('res.partner.address', 'Technician'),
            'customer': fields.many2one('res.partner', 'Customer', domain=[('customer', '=', True)]),
            'cust_address': fields.many2one('res.partner.address', 'Address'),
            'production_id': fields.many2one('mrp.production', 'Production'),
            'street': fields.char('Street', size=128),
            'zip': fields.char('Zip', change_default=True, size=24),
            'city': fields.char('City', size=128),
            'notice_date': fields.date('Notice Date'),
            'assign_date': fields.date('Assignation Date'),
            'consultation_date': fields.date('Consultation Date'),
            'installation_date': fields.date('Installation Date'),
            'agreement': fields.many2one('inv.agreement', 'Agreement'),
            'state':fields.selection([
                ('active','Active'),
                ('inactive','Inactive'),
                ('cancel','Canceled'),
                ('nouse','No Used')], 'State', readonly=True),
    }
    
    _defaults = {  
        'state': lambda *a: 'nouse',
    }
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}
        if len(args) > 2 and args[2]:
            if args[2][0] == 'mac':
                args.pop(2) 
        return  super(stock_production_lot, self).search(cr, uid, args, offset, limit, order, context, count)
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=None):
        ids = []
        res = False
        is_mac = False
        if len(args) > 2 and args[2]:
            if args[2][0] == 'mac':
                args.pop(2)
                is_mac = True
        res = super(stock_production_lot,self).name_search(cr, uid, name, args, operator, context, limit)
        if not res:
            args.append(('prefix', 'ilike', name))
            ids = self.search(cr, uid, args)
            if not res and is_mac:
                seq = name.split('/')
                values = {
                    'name': seq[1],
                    'prefix': seq[0], 
                    'product_id': args[0][2],
                }
                ids.append(self.create(cr, uid, values))
        if ids:
            res = self.name_get(cr, uid, ids, context)
        return res
    
    def default_get(self, cr, uid, fields, context=None):
        partner_obj = self.pool.get('res.partner')
        if context is None:
            context = {}
        res = super(stock_production_lot, self).default_get(cr, uid, fields, context)
        if 'partner' in context:
            ids = partner_obj.search(cr, uid, [('name', '=', context['partner'])])
            for partner in partner_obj.browse(cr, uid, ids):
                res.update({
                    'customer': partner.id,
                    'cust_address': partner.address[0].id,
                })
        return res
    
    def onchange_customer(self, cr, uid, ids, customer_id, context=None):
        res = {}
        if customer_id:
            address_id = self.pool.get('res.partner.address').search(cr, uid, [('partner_id', '=', customer_id)])[0]
            res = {
                'cust_address': address_id,
            }
        return {'value': res}
    
    def onchange_address(self, cr, uid, ids, address_id, context=None):
        res = {}
        if address_id:
            address = self.pool.get('res.partner.address').browse(cr, uid, address_id)
            res = {
                'street': address.street,
                'zip': address.zip,
                'city': address.city,
            }
        return {'value': res}
    
    def action_active(self, cr, uid, ids):
        for id in ids:
            lot = self.browse(cr, uid, id)
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': id,
                 'rec_state': 'Active',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            if lot.agreement:
                self.pool.get('inv.agreement').set_process(cr, uid, [lot.agreement.id])
            self.write(cr, uid, ids, {'state': 'active'})
        return True
        
    def action_inactive(self, cr, uid, ids): 
        for id in ids:
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': id,
                 'rec_state': 'Inactive',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
#            if lot.agreement:
#                self.pool.get('inv.agreement').set_done(cr, uid, [lot.agreement.id])
#                self.pool.get('inv.agreement').set_draft(cr, uid, [lot.agreement.id])
            self.write(cr, uid, ids, {'state': 'inactive'})
        return True
        
    def action_nouse(self, cr, uid, ids):
        wf_service = netsvc.LocalService("workflow")
        order_obj = self.pool.get('mrp.production')
        for lot in self.browse(cr, uid, ids):
            
#            if lot.production_id:
#                prod_values = {
#                    'product_id': lot.production_id.product_id.id,
#                    '': ,
#                    '': ,
#                    '': ,
#                    '': ,
#                }
#                prod_id = order_obj.create(cr, uid, prod_values)
#                if order_obj.browse(cr, uid, prod_id).state == 'confirmed':
#                    order_obj.force_production(cr, uid, id)
#                wf_service.trg_validate(uid, 'mrp.production', prod_id, 'button_produce', cr)
#                wf_service.trg_validate(uid, 'mrp.production', prod_id, 'button_produce_done', cr)
                
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': lot.id,
                 'rec_state': 'No Used',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, ids, {'state': 'nouse'})
        return True
        
    def action_cancel(self, cr, uid, ids): 
        for id in ids:
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': id,
                 'rec_state': 'Canceled',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, ids, {'state': 'cancel'})
        return True
stock_production_lot()

class stock_prodlot_history(osv.osv):

    _name = 'stock.prodlot.history'
    _description = 'Product Lot Movement History'
 
    _columns = {
            'description':fields.char('Description', size=64),
            'prodlot_id': fields.many2one('stock.production.lot', required=True),
            'date': fields.date('Date', required=True, readonly=True),
            'rec_state': fields.char('state', size=64, required=True, readonly=True),
    }
stock_prodlot_history()