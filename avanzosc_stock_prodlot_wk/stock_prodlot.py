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
            'technician': fields.many2one('res.partner.contact', 'Technician'),
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
            'is_service': fields.boolean('Is Service'),
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
        is_mac = False
        if len(args) > 2 and args[2]:
            if args[2][0] == 'is_service':
                is_mac = True
                args.pop(2) 
        res = super(stock_production_lot, self).search(cr, uid, args, offset, limit, order, context, count)
        if is_mac == False:
            if not res:
                if args[0][0] == 'product_id':
                    args.pop(0) 
                    res = super(stock_production_lot, self).search(cr, uid, args, offset, limit, order, context, count)
        return res
    

        
        
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=None):
        ids = []
        limit=0
        res = False
        is_mac = False
        res = super(stock_production_lot,self).name_search(cr, uid, name, args, operator, context, limit)
        if len(args) > 2 and args[2]:
            if args[2][0] == 'is_service':
#                args.pop(2)
                is_mac = True
        if is_mac == False:
            if context.get('src_model') == 'mrp.lot.configurator.list':
                if not res and len(args)==2:
                    if args[0][0] == 'product_id':
                        args.pop(0)
                    elif args[1][0] == 'product_id':
                        args.pop(1)
                    res = self.name_search(cr, uid, name, args, operator, context, limit)
                    return res
        if not res:
            if '/' in name:
                seq = name.split('/')
                res = super(stock_production_lot,self).name_search(cr, uid, seq[1], args, operator, context, limit)
            else:
                res = super(stock_production_lot,self).name_search(cr, uid, name, args, operator, context, limit)
        if not res:
            args.append(('prefix', 'ilike', name))
            ids = self.search(cr, uid, args)
            if not res and is_mac:
                seq = name.split('/')
                if len(seq) < 2:
                    raise osv.except_osv(_('Invalid MAC/SERIAL!'), _('You must insert both references, MAC and Serial!'))
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
        values = {}
        agr_obj = self.pool.get('inv.agreement')
        for lot in self.browse(cr, uid, ids):
            if lot.is_service:
                if lot.agreement:
                    agr_obj.set_draft(cr, uid, [lot.agreement.id])
                    agr_obj.set_process(cr, uid, [lot.agreement.id])
                    name = agr_obj.name_get(cr, uid, [lot.agreement.id])[0][1]
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'Active', 
                         'description': _('Service activated for agreement: %s') % (name)
                     }
                else:
                    raise osv.except_osv(_('Invalid action !'), _('System could not find the agreement !'))
            else:
                if lot.agreement:
                    name = agr_obj.name_get(cr, uid, [lot.agreement.id])[0][1]
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'Active', 
                         'description': _('Lot activated for agreement: %s') % (name)
                    }
                else:
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'Active',
                         'description': _('Lot actived')
                    }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, lot.id, {'state': 'active'})
        return True
        
    def action_inactive(self, cr, uid, ids): 
        values = {}
        wf_service = netsvc.LocalService("workflow")
        agr_obj = self.pool.get('inv.agreement')
        for lot in self.browse(cr, uid, ids):
            if lot.is_service:
                if lot.agreement:
   #                    agr_obj.set_done(cr, uid, [lot.agreement.id])        
                    name = agr_obj.name_get(cr, uid, [lot.agreement.id])[0][1]
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'Inactive', 
                         'description': _('Service inactived, agreement %s allready running.') % (name)
                     }
                    item_ids = self.search(cr, uid, [('agreement', '=', lot.agreement.id), ('is_service', '=', False)])
                    for item_id in item_ids:
                            wf_service.trg_validate(uid, 'stock.production.lot', item_id, 'button_inactive', cr)
                else:
                    raise osv.except_osv(_('Invalid action !'), _('System could not find the agreement !'))
            else:
                if lot.agreement:
                    name = agr_obj.name_get(cr, uid, [lot.agreement.id])[0][1]
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'Inactive', 
                         'description': _('Lot inactived for agreement: %s') % (name)
                    }
                else:
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'Inactive',
                         'description': _('Lot inactived')
                    }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, lot.id, {'state': 'inactive'})
        return True
        
    def action_nouse(self, cr, uid, ids):
        context = {}
        wf_service = netsvc.LocalService("workflow")
        order_obj = self.pool.get('mrp.production')
        move_obj = self.pool.get('stock.move')
        prod_line = self.pool.get('mrp.production.product.line')
        prod_produce = self.pool.get('mrp.product.produce')
        agr_obj = self.pool.get('inv.agreement')
        for lot in self.browse(cr, uid, ids):
            if lot.is_service:
                if lot.agreement:
                    move_lines = []
                    move_created = []
                    agr_obj.set_done(cr, uid, [lot.agreement.id])
                    name = agr_obj.name_get(cr, uid, [lot.agreement.id])[0][1]
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'No Used', 
                         'description': _('Service no used for agreement: %s') % (name)
                     }
                    
                    if lot.production_id:
                        new_id = order_obj.copy(cr, uid, lot.production_id.id)
                        prod_vals = {
                            'name': lot.production_id.name + ' (RETURNED)',
                            'date_planned': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'location_src_id': lot.production_id.location_dest_id.id,
                            'location_dest_id': lot.production_id.location_src_id.id,
                        }
                        order_obj.write(cr, uid, [new_id], prod_vals)
                        order_lines = []
                        for line in lot.production_id.product_lines:
                            new_line_id = prod_line.copy(cr, uid, line.id)
                            order_lines.append(new_line_id)
                        order_obj.write(cr, uid, [new_id], {'product_lines':  [(6,0,order_lines)]})
                        for line in lot.production_id.move_lines2:
                            new_line_id = move_obj.copy(cr, uid, line.id)
                            move_line_vals ={
                                'location_id': lot.production_id.location_dest_id.id,
                                'location_dest_id': lot.production_id.location_src_id.id,
                                'prodlot_id': line.prodlot_id.id,
                            }
                            move_lines.append(new_line_id)
                        for line in lot.production_id.move_created_ids2:
                            new_line_id = move_obj.copy(cr, uid, line.id)
                            created_line_vals ={
                                'location_id': line.location_dest_id.id,
                                'location_dest_id': line.location_id.id,
                                'prodlot_id': line.prodlot_id.id,
                            }
                            move_created.append(new_line_id)
                        order_obj.write(cr, uid, [new_id], {'move_lines':  [(6,0,move_lines)], 'move_created_ids':  [(6,0,move_created)]})
                        order = order_obj.browse(cr, uid, new_id)
                        wf_service.trg_validate(uid, 'mrp.production', new_id, 'button_confirm', cr)
                        wf_service.trg_validate(uid, 'mrp.production', new_id, 'button_configure', cr)
                        active_move_ids = []
                        for move in order.move_lines:
                            move_obj.write(cr, uid, [move.id], move_line_vals)
                            active_move_ids.append(move.id)
                        for move in order.move_created_ids:
                            move_obj.write(cr, uid, [move.id], created_line_vals)
                            active_move_ids.append(move.id)
                        if order.state == 'confirmed':
                            order_obj.force_production(cr, uid, [new_id])
                        wf_service.trg_validate(uid, 'mrp.production', new_id, 'button_produce', cr)
                        wf_service.trg_validate(uid, 'mrp.production', new_id, 'button_produce_done', cr)
                        context.update({
                            'active_model': 'mrp.production',
                            'active_ids': [new_id],
                            'active_id': new_id,
                        })
                        order_obj.action_produce(cr, uid, new_id, order.product_qty, 'consume_produce', context=context)
                        item_ids = self.search(cr, uid, [('agreement', '=', lot.agreement.id), ('is_service', '=', False)])
                        for item_id in item_ids:
                            wf_service.trg_validate(uid, 'stock.production.lot', item_id, 'button_nouse', cr)
                else:
                    raise osv.except_osv(_('Invalid action !'), _('System could not find the agreement !'))
            else:
                if lot.agreement:
                    name = agr_obj.name_get(cr, uid, [lot.agreement.id])[0][1]
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'No Used', 
                         'description': _('Lot no used for agreement: %s') % (name)
                    }
                else:
                    values = {
                         'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'prodlot_id': lot.id,
                         'rec_state': 'No Used',
                         'description': _('Lot no used')
                    }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, ids, {'state': 'nouse'})
        return True
        
    def action_cancel(self, cr, uid, ids): 
        for lot in self.browse(cr, uid, ids):
            if lot.is_service:
                values = {
                     'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'prodlot_id': lot.id,
                     'rec_state': 'Canceled', 
                     'description': _('Service canceled')
                }
            else:
                values = {
                     'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'prodlot_id': lot.id,
                     'rec_state': 'Canceled', 
                     'description': _('Lot removed')
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