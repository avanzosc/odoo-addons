
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    Date: 13/11/2013
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class product_template(osv.osv): 

    _description = 'product template Inheritance'
    _inherit = 'product.template'
    
    _columns = {
                'supply_method': fields.selection([('produce','Produce'),('buy','Buy'),('buy/produce','Buy/Produce')], 'Supply method', required=True, help="Produce will generate production order or tasks, according to the product type. Purchase will trigger purchase orders when requested."),
                }
    
product_template()

class sale_order_line(osv.osv):
        
    _description = 'sale order line Inheritance'
    _inherit = 'sale.order.line'

    _columns = {
                'supply_method': fields.selection([('produce','Produce'),('buy','Buy')], 'Supply method', required=True),
                }
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist=pricelist, product=product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag)
        
        if product:
            product_obj = self.pool.get('product.product')
            product_reg = product_obj.browse(cr, uid, product)
            product_supmet= product_reg.supply_method # product supply method
            if product_supmet !='buy/produce' :
                res['value']['supply_method'] = product_reg.supply_method
            #if 'supply_method' in res['value']:
            #    if res['value']['supply_method'] == 'buy':
             #       res['value']['type'] = 'make_to_stock'
        return res 

sale_order_line()

class procurement_order (osv.osv):
    
    _description = 'sale order line Inheritance'
    _inherit = 'procurement.order'
    
    def check_produce(self, cr, uid, ids, context=None):
        print '***** ESTOY EN CHECK_PRODUCE'        
        product_lst = []
        for procurement in self.browse(cr, uid, ids, context=context):  # tratar todos los productos 'buy/produce'
            if procurement.product_id.product_tmpl_id.supply_method == 'buy/produce':
                product_id = procurement.product_id.id
                product_lst.append(product_id)
                so_line_supmet = procurement.move_id.sale_line_id.supply_method
                product_obj = self.pool.get('product.product')
                product_obj.write(cr,uid,[product_id],{'supply_method': so_line_supmet})
        res = super(procurement_order, self).check_produce(cr, uid, ids, context=context)
        if product_lst:  # restaurar todos los productos 'buy/produce'
            product_obj.write(cr,uid,product_lst,{'supply_method': 'buy/produce'})
        return res
    
    def check_buy(self, cr, uid, ids):
        print '***** ESTOY EN CHECK BUY'
        product_lst = []
        for procurement in self.browse(cr, uid, ids): # tratar todos los productos 'buy/produce'
            if procurement.product_id.product_tmpl_id.supply_method == 'buy/produce':
                product_id = procurement.product_id.id
                product_lst.append(product_id)
                so_line_supmet = procurement.move_id.sale_line_id.supply_method
                product_obj = self.pool.get('product.product')
                product_obj.write(cr,uid,[product_id],{'supply_method': so_line_supmet})
        res = super(procurement_order, self).check_buy(cr, uid, ids)
        if product_lst:  # restaurar todos los productos 'buy/produce'
            product_obj.write(cr,uid,product_lst,{'supply_method': 'buy/produce'})
        return res
    
procurement_order()


