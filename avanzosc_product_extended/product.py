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
from osv import osv, fields
import decimal_precision as dp
import time

from tools.translate import _

class product_product(osv.osv):
    _inherit="product.product"
    _columns = {
                'last_purchase_price':fields.float('Last purchase price',  readonly=True),
                'last_purchase_date':fields.date('Last purchase date',  readonly=True),
                'last_sale_price':fields.float('Last sale price',  readonly=True),
                'last_sale_date':fields.date('Last sale date',  readonly=True),
                'last_manufacturing_cost':fields.float('Last manufacturing cost',  readonly=True),
                'last_manufacturing_end_date':fields.date('Last manufacturing end date',  readonly=True),
                'standard_cost':fields.float('Standard cost'),  
                }
product_product()


class sale_order(osv.osv):
    _inherit = "sale.order"
    
    
    def action_wait(self, cr, uid, ids, *args):
        
        res = super(sale_order, self).action_wait(cr, uid, ids, *args)
        for o in self.browse(cr, uid, ids):
            for line in o.order_line:
                if line.product_id:
                    self.pool.get('product.product').write(cr,uid,[line.product_id.id],({'last_sale_date': time.strftime('%Y-%m-%d %H:%M:%S')}))   
        return True
    
sale_order()


class purchase_order(osv.osv):
    _inherit = "purchase.order"
    
    
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        res = super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)
        for o in self.browse(cr, uid, ids):
            for line in o.order_line:
                if line.product_id:
                    self.pool.get('product.product').write(cr,uid,[line.product_id.id],({'last_purchase_date': time.strftime('%Y-%m-%d %H:%M:%S')}))   
        return True
    
purchase_order()


class account_invoice(osv.osv):
    _inherit = "account.invoice"
    
    def action_date_assign(self, cr, uid, ids, *args):
        res = super(account_invoice, self).action_date_assign(cr, uid, ids, *args)
        for o in self.browse(cr,uid,ids):
            for line in o.invoice_line:
                if line.product_id:
                    if (o.type == 'out_invoice'):
                        self.pool.get('product.product').write(cr,uid,[line.product_id.id],({'last_sale_price': line.price_unit}))
                    elif (o.type == 'in_invoice'):
                        self.pool.get('product.product').write(cr,uid,[line.product_id.id],({'last_purchase_price': line.price_unit}))
        return True
    
account_invoice()
