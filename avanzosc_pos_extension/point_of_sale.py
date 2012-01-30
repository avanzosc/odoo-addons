
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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import pooler
import netsvc
from osv import osv, fields
from tools.translate import _


class pos_make_payment(osv.osv_memory):

    _inherit='pos.make.payment'
    
    _columns = {
                'ticket_amount':fields.float('Ticket amount', digits = (10,2)),
                'pay_amount':fields.float('Pay amount', digits = (10,2)),
                'return': fields.float('Exchange', digits = (10,2)),
                }
    
    def on_change_amount(self, cr, uid, ids, pay, ticket, context=None):
        res = {}
        val= 0.0
        if not pay:
            pay=0.0
        if not ticket:
            ticket=0.0
        if ticket <= pay:
            val = pay - ticket 
        res ={'value': {'return': val}}
        return res
    def default_get(self, cr, uid, fields, context=None):
        
        res = super(pos_make_payment, self).default_get(cr,uid,fields,context)
        if 'amount' in res.keys():
            amount = res['amount']
        else:
            amount=0.0
        res.update({'ticket_amount':amount})
        return res
    
    def check(self,cr,uid,ids,context=None):
        res={}
        order_obj = self.pool.get('pos.order')
        pos_obj = self.pool.get('pos.make.payment')
        if context is None:
            context = {}
        active_id = context and context.get('active_id', False)
        order = order_obj.browse(cr, uid, active_id, context=context)
        pos = pos_obj.browse(cr,uid, ids[0], context=context)
        if (int(pos.pay_amount) < int(pos.amount)):
               pos_obj.write(cr,uid,[pos.id],{'amount':pos.pay_amount})
        order_obj.write(cr, uid, [order.id], {'name': self.pool.get('ir.sequence').get(cr, uid, 'pos.order')}),
        super(pos_make_payment, self).check(cr, uid, ids, context=context)   
        if pos.invoice_wanted:
            res = order_obj.print_invoice_report(cr,uid,ids, context)   
        else:  
            res = self.pool.get('pos.receipt').print_report(cr, uid, ids, context)
        return res
    
    
    
    
pos_make_payment()

class pos_order(osv.osv):
    _inherit="pos.order"
    _defaults={
               'name': lambda obj, cr, uid, context: "/",
               }
    
    
    def print_invoice_report(self, cr, uid, ids, context=None):
        """
        To get the date and print the report
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param context: A standard dictionary
        @return : retrun report
        """
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'pos.invoice',
            'datas': datas,
        }
pos_order()

class pos_order_line(osv.osv):
    _inherit = "pos.order.line"
    _columns = {
                'real_stock':fields.related('product_id', 'qty_available', type='float', relation='product.product', string='Real Stock', store=True, readonly=True),
                'virtual_stock':fields.related('product_id', 'virtual_available', type='float', relation='product.product', string='Virtual Stock', store=True, readonly=True),
                }
    def onchange_product_id(self, cr, uid, ids, pricelist,product_id, qty=0, partner_id=False):
        res = {}
        if product_id:
             product_obj=self.pool.get('product.product').browse(cr,uid,product_id)
             res = super(pos_order_line, self).onchange_product_id(cr,uid,ids,pricelist, product_id, qty, partner_id)
             res['value'].update({'real_stock':product_obj.qty_available, 'virtual_stock':product_obj.virtual_available})
        return res
pos_order_line()