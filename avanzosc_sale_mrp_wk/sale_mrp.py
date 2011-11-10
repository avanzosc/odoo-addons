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

class sale_order(osv.osv):

    _inherit='sale.order'
    
    def _count_meetings(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        meeting_obj = self.pool.get('crm.meeting')
        for id in ids:
            res[id] = len(meeting_obj.search(cr, uid, [('sale_order_id', '=', id)]))
        return res
 
    _columns = {
        'order_line': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, states={'draft': [('readonly', False)], 'waiting_install': [('readonly', False)]}),
        'meeting_num': fields.function(_count_meetings, method=True, type='integer', string='Nº Meetings'),
        'state': fields.selection([
            ('draft', 'Quotation'),
            ('waiting_install', 'Waiting Installation'),
            ('waiting_date', 'Waiting Schedule'),
            ('manual', 'Manual In Progress'),
            ('progress', 'In Progress'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
            ], 'Order State', readonly=True, help="Gives the state of the quotation or sales order. \nThe exception state is automatically set when a cancel operation occurs in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception). \nThe 'Waiting Schedule' state is set when the invoice is confirmed but waiting for the scheduler to run on the date 'Ordered Date'.", select=True),
    }
    
    def action_wait_install(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'waiting_install'})
        return True
    
    def is_analytic(self, cr, uid, ids, context=None):
        for sale in self.browse(cr, uid, ids):
            if sale.order_policy == 'analytic' and not sale.project_id:
                return False
        return True
    
sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def create(self, cr, uid, vals, context=None):
        if 'pack_parent_line_id' in vals:
            date = self.pool.get('sale.order').browse(cr, uid, vals['order_id']).agreement_date or False
            if date:
                vals.update({'invoice_date': date})
        return super(sale_order_line,self).create(cr, uid, vals, context)
    
sale_order_line()