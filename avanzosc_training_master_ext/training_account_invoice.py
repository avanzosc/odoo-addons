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

class training_account_invoice(osv.osv):
    _inherit='account.invoice'
    
    def _paid(self, cr, uid, ids, name, args, context=None):
        res = {}
        paid=0
        for invoice in self.browse(cr, uid, ids, context=context):
            paid=(invoice.amount_total)-(invoice.residual)
            res[invoice.id]=paid
        return res
    
    def _contact(self, cr, uid, ids, name, args, context=None):
        res = {}
        training_sale_order_obj = self.pool.get('sale.order')
        for invoice in self.browse(cr, uid, ids, context=context):
            order=invoice.origin
            list_id_sale_orders = training_sale_order_obj.search(cr,uid,[('name','=', order)])
            contact=''
            for sale_order in training_sale_order_obj.browse(cr,uid,list_id_sale_orders,context=context):
                name = sale_order.contact_id.name or ''
                lastname_two=sale_order.contact_id.lastname_two or ''
                firstname=sale_order.contact_id.first_name or ''
                contact=name+' '+lastname_two+' '+firstname
            res[invoice.id]=contact
        return res
    
    _columns = {
        
        'paid':fields.function(_paid, type='float',method=True, string='Paid'),
        'contact':fields.function(_contact, type='char',method=True, string='Contact'),
    
    }
training_account_invoice()