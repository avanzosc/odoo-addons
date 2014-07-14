# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
#    Date: 05/06/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import decimal_precision as dp

from _common import rounding

class purchase_order_line(osv.osv):
    _inherit="purchase.order.line"
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty, uom,
            partner_id, qty_uos=0, uos=False, date_order=False, fiscal_position=False, date_planned=False,
            name=False, price_unit=False, notes=False, context={}):

        if not product:
            return {'value': {'price_unit': price_unit or 0.0, 'name': name or '',
                'notes': notes or'', 'product_uom' : uom or False}, 'domain':{'product_uom':[]}}

        res = {}
        
        res = super(purchase_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order, fiscal_position, date_planned, name, price_unit, notes)
        
        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)

        prod_uos = prod.uos_id.id
        if uos <> prod_uos:
            uos = prod_uos

        qty = qty or 0.0
        #qty = rounding(qty, product.uom_id.rounding)
        sec_price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                    product, qty or 1.0, partner_id, {'uom': uom, 'date': date_order})[pricelist]        
        try:
            sec_price = sec_price * prod.coef_amount
        except ZeroDivisionError:
            pass

        res['value']['product_qty'] = qty
        res['value']['product_uos'] = uos
        res['value']['product_uos_qty'] = qty / prod.coef_amount
        res['value']['secondary_price'] = sec_price
        
        return res

    def uos_change(self, cr, uid, ids, product_uos, product_uos_qty=0, product_id=None, context=None):
        if context == None:
            context = {}
        
        product_obj = self.pool.get('product.product')
        if not product_id:
            return {'value': {'product_uom': product_uos,
                'product_qty': product_uos_qty}, 'domain': {}}

        product = product_obj.browse(cr, uid, product_id, context=context)
        value = {
            'product_uom': product.uom_id.id,
        }
        
        try:
            value.update({
                'product_qty': rounding(product_uos_qty * product.coef_amount, product.uom_id.rounding)
            })
        except ZeroDivisionError:
            pass
        return {'value': value}
    
    def uom_change(self, cr, uid, ids, product_uom, product_uom_qty=0, product_id=None, context=None):
        if context == None:
            context = {}
        
        product_obj = self.pool.get('product.product')
        if not product_id:
            return {'value': {'product_uos': product_uom,
                'product_uos_qty': product_uom_qty}, 'domain': {}}
        product = product_obj.browse(cr, uid, product_id)
        value = {
            'product_uos': product.uos_id.id,
            'product_uos_qty': rounding(product_uom_qty / product.coef_amount, product.uos_id.rounding),
        }
        return {'value': value}
    
    def calculate_secondary_price(self, cr, uid, ids, field_name, arg, context=None):
        if context == None:
            context = {}
        
        res = {}
        for po_line in self.browse(cr, uid, ids, context=context):
            price = po_line.price_unit
            prod = self.pool.get('product.product').browse(cr, uid, po_line.product_id.id, context=context)
            try:
                price = price * prod.uos_coeff
            except ZeroDivisionError:
                pass

            res[po_line.id] = price
        return res
    
    _columns = {
        'product_uos_qty': fields.float('Quantity (UoS)' ,digits_compute = dp.get_precision('Product UoS'), 
                                        readonly=True, states={'draft': [('readonly', False)]}),
        'product_uos': fields.many2one('product.uom', 'Product UoS'),
        'secondary_price': fields.function(calculate_secondary_price, method=True, string='Price',
                                        type="float", store=False),
    }
    
    _defaults = {
        'product_qty': lambda *a: 0.0,
        'product_uos_qty': lambda*a: 0.0,
    }
    
purchase_order_line()

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    
    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        res = {}
        
        res = super(purchase_order, self)._prepare_inv_line(cr, uid, account_id, order_line, context)
        
        res['sec_qty'] = order_line.product_uos_qty   
        res['sec_uom_id'] = order_line.product_uos.id
        
        return res
    
purchase_order()