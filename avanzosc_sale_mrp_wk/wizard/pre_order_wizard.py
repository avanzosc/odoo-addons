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
import time
import netsvc
from tools.translate import _
from osv import osv
from osv import fields

class pre_order_wizard(osv.osv_memory):
    _name = 'pre.order.wizard'
    _description = 'Pre-Order Wizard to create a meeting'
 
    _columns = {
        'date': fields.datetime('Date', required=True),
        'date_deadline': fields.datetime('Deadline', required=True),
        'section_id': fields.many2one('crm.case.section', 'Sales Team'),
        'meeting_created': fields.boolean('Meeting'),
    }
    
    _defaults = {  
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'date_deadline': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        if context == None:
            context = {}
        res = super(pre_order_wizard, self).default_get(cr, uid, fields_list, context)
        if 'active_id' in context.keys():
            meeting_id = self.pool.get('crm.meeting').search(cr, uid, [('sale_order_id', '=', context['active_id'])])
            if not meeting_id:
                res.update({'meeting_created': True})
            else:
                res.update({'meeting_created': False})
        return res
    
    def create_meeting(self, cr, uid, ids, context=None):
        values = {}
        wf_service = netsvc.LocalService("workflow")
        meeting_obj = self.pool.get('crm.meeting')
        sale_obj = self.pool.get('sale.order')
        
        for wizard in self.browse(cr, uid, ids):
            for sale in sale_obj.browse(cr, uid, context['active_ids']):
                values = {
                    'name': _('Install:')+' '+ sale.name,
                    'partner_id': sale.partner_id.id,
                    'date': wizard.date,
                    'date_deadline': wizard.date_deadline,
                    'section_id': wizard.section_id.id,
                    'sale_order_id': sale.id,
                    'location': sale.partner_shipping_id.city,
                }
                meeting_obj.create(cr, uid, values)
                wf_service.trg_validate(uid, 'sale.order', sale.id, 'button_install', cr)
        return {'type': 'ir.actions.act_window_close'}
    
    def skip_meeting(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        sale_obj = self.pool.get('sale.order')
        for wizard in self.browse(cr, uid, ids):
            for sale in sale_obj.browse(cr, uid, context['active_ids']):
                wf_service.trg_validate(uid, 'sale.order', sale.id, 'button_install', cr)
        return {'type': 'ir.actions.act_window_close'}
    
pre_order_wizard()