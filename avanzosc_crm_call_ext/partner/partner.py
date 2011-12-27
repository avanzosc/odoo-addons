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

class res_partner(osv.osv):
    _inherit = 'res.partner'
 
 
    def _calculate_running_agree_num(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        agreement_obj = self.pool.get('inv.agreement')
        for id in ids:
            res[id] = len(agreement_obj.search(cr, uid, [('partner_id', '=', id), ('state', '=', 'running')]))
        return res
    
    def _calculate_done_agree_num(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        agreement_obj = self.pool.get('inv.agreement')
        for id in ids:
            res[id] = len(agreement_obj.search(cr, uid, [('partner_id', '=', id), ('state', '=', 'done')]))
        return res
    
    def _calculate_inactive_service_num(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        service_obj = self.pool.get('stock.production.lot')
        for id in ids:
            res[id] = len(service_obj.search(cr, uid, [('customer', '=', id), ('state', '=', 'inactive'), ('is_service','=',True)]))
        return res
    
    def _calculate_active_service_num(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        service_obj = self.pool.get('stock.production.lot')
        for id in ids:
            res[id] = len(service_obj.search(cr, uid, [('customer', '=', id), ('state', '=', 'active'), ('is_service','=', True)]))
        return res
    
    _columns = {
            'helpdesk_ids': fields.one2many('crm.helpdesk', 'partner_id', 'HelpDesks'),
            'claim_ids': fields.one2many('crm.claim', 'partner_id', 'Claims'),
            'running_agree_num':fields.function(_calculate_running_agree_num, method=True, type='integer', string='Nº Running agreement'),
            'done_agree_num':fields.function(_calculate_done_agree_num, method=True, type='integer', string='Nº Done agreement'),
            'inactive_service_num':fields.function(_calculate_inactive_service_num, method=True, type='integer', string='Nº Inactive Service'),
            'active_service_num':fields.function(_calculate_active_service_num, method=True, type='integer', string='Nº Active Service'),
        }
res_partner()