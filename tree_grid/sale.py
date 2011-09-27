##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields
from tools.translate import _

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

class sale_order_line(osv.osv):
    
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
 
            
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
#        if not pricelist:
#            raise osv.except_osv(_('No Pricelist !'), _('You have to select a pricelist or a supplier in the purchase form !\nPlease set one before choosing a product.'))
#        if not  partner_id:
#            raise osv.except_osv(_('No Partner!'), _('You have to select a partner in the purchase form !\nPlease set one partner before choosing a product.'))
        if not product:
            return {'value': {'th_weight': 0, 'product_packaging': False,
                'product_uos_qty': qty, 'tax_id':[]}, 'domain': {'product_uom': [],
                   'product_uos': []}, 'domain':{'product_uom':[]}}
        res = {}
        prod= self.pool.get('product.product').browse(cr, uid, product)

        product_uom_pool = self.pool.get('product.uom')
        lang=False
        if partner_id:
            lang=self.pool.get('res.partner').read(cr, uid, partner_id, ['lang'])['lang']
        context={'lang':lang}
        context['partner_id'] = partner_id

        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        prod_uom_po = prod.uom_po_id.id
        if not uom:
            uom = prod_uom_po
        if not date_order:
            date_order = time.strftime('%Y-%m-%d')
        qty = qty or 1.0
        seller_delay = 0

        prod_name = self.pool.get('product.product').name_get(cr, uid, [prod.id], context=context)[0][1]
        res = {}
        for s in prod.seller_ids:
            if s.name.id == partner_id:
                seller_delay = s.delay
                if s.product_uom:
                    temp_qty = product_uom_pool._compute_qty(cr, uid, s.product_uom.id, s.min_qty, to_uom_id=prod.uom_id.id)
                    uom = s.product_uom.id #prod_uom_po
                temp_qty = s.min_qty # supplier _qty assigned to temp
                if qty < temp_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    qty = temp_qty
                    res.update({'warning': {'title': _('Warning'), 'message': _('The selected supplier has a minimal quantity set to %s, you cannot purchase less.') % qty}})
        qty_in_product_uom = product_uom_pool._compute_qty(cr, uid, uom, qty, to_uom_id=prod.uom_id.id)
        price = self.pool.get('product.pricelist').price_get(cr,uid,[pricelist],
                    product, qty_in_product_uom or 1.0, partner_id, {
                        'uom': uom,
                        'date': date_order,
                        })[pricelist]
        dt = (datetime.now() + relativedelta(days=int(seller_delay) or 0.0)).strftime('%Y-%m-%d %H:%M:%S')


        res.update({'value': {'price_unit': price, 'name': prod_name,
            'taxes_id':map(lambda x: x.id, prod.supplier_taxes_id),
#            'date_planned': date_planned or dt,'notes': notes or prod.description_purchase,
            'product_qty': qty,
            'product_uom': uom}})
        
        
        domain = {}

        taxes = self.pool.get('account.tax').browse(cr, uid,map(lambda x: x.id, prod.supplier_taxes_id))
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        res['value']['taxes_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, taxes)

        res2 = self.pool.get('product.uom').read(cr, uid, [uom], ['category_id'])
        res3 = prod.uom_id.category_id.id
        domain = {'product_uom':[('category_id','=',res2[0]['category_id'][0])]}
        if res2[0]['category_id'][0] != res3:
            raise osv.except_osv(_('Wrong Product UOM !'), _('You have to select a product UOM in the same category than the purchase UOM of the product'))
        
        res['domain'] = domain       

        return res
    
    
    
    
    
#    
#    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
#            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
##        if not  partner_id:
##            raise osv.except_osv(_('No Customer Defined !'), _('You have to select a customer in the sales form !\nPlease set one customer before choosing a product.'))
#        res={}
#        product_uom_qty = 0.0
#        product_packaging = False
#        delay = False
#        tax_id = False
#        type = False
#        name = False
#        product_uom = False
#        product_uos = False
#        product_uos_qty = 0.0
#        th_weigth = 0.0
#        price_unit = 0.0
#        
#        product_uom_obj = self.pool.get('product.uom')
#        partner_obj = self.pool.get('res.partner')
#        product_obj = self.pool.get('product.product')
#        if partner_id:
#            lang = partner_obj.browse(cr, uid, partner_id).lang
#            context = {'lang': lang, 'partner_id': partner_id}
#
#        if not product:
#            return {'value': {'th_weight': 0, 'product_packaging': False,
#                'product_uos_qty': qty, 'tax_id':[]}, 'domain': {'product_uom': [],
#                   'product_uos': []}}
#        if not date_order:
#            date_order = time.strftime('%Y-%m-%d')
#
#        
#        product_obj = product_obj.browse(cr, uid, product, context=context)
##        if not packaging and product_obj.packaging:
##            packaging = product_obj.packaging[0].id
##            product_packaging = packaging
##
##        if packaging:
##            default_uom = product_obj.uom_id and product_obj.uom_id.id
##            pack = self.pool.get('product.packaging').browse(cr, uid, packaging, context=context)
##            q = product_uom_obj._compute_qty(cr, uid, uom, pack.qty, default_uom)
###            qty = qty - qty % q + q
##            if qty and (q and not (qty % q) == 0):
##                ean = pack.ean or _('(n/a)')
##                qty_pack = pack.qty
##                type_ul = pack.ul
##                warn_msg = _("You selected a quantity of %d Units.\n"
##                            "But it's not compatible with the selected packaging.\n"
##                            "Here is a proposition of quantities according to the packaging:\n\n"
##                            "EAN: %s Quantity: %s Type of ul: %s") % \
##                                (qty, ean, qty_pack, type_ul.name)
##                res['warning'] = {
##                    'title': _('Picking Information !'),
##                    'message': warn_msg
##                    }
##            product_uom_qty= qty
#
#        uom2 = False
#        if uom:
#            uom2 = product_uom_obj.browse(cr, uid, uom)
#            if product_obj.uom_id.category_id.id != uom2.category_id.id:
#                uom = False
#        if uos:
#            if product_obj.uos_id:
#                uos2 = product_uom_obj.browse(cr, uid, uos)
#                if product_obj.uos_id.category_id.id != uos2.category_id.id:
#                    uos = False
#            else:
#                uos = False
#        if product_obj.description_sale:
#             notes=product_obj.description_sale
#        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
#        if update_tax: #The quantity only have changed
#            delay = product_obj.sale_delay or 0.0
#            tax_id = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)
#            type =  product_obj.procure_method
#        if not flag:
#            name = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context)[0][1]
#       
#        if (not uom) and (not uos):
#            product_uom = product_obj.uom_id.id
#            if product_obj.uos_id:
#                product_uos = product_obj.uos_id.id 
#                product_uos_qty = qty * product_obj.uos_coeff
#                uos_category_id = product_obj.uos_id.category_id.id
#            else:
#                product_uos= False
#                product_uos_qty = qty
#                th_weight = qty * product_obj.weight
#                uos_category_id = False
##            res['domain'] = {'product_uom':
##                        [('category_id', '=', product_obj.uom_id.category_id.id)],
##                        'product_uos':
##                        [('category_id', '=', uos_category_id)]}
#    
#        elif uos and not uom: # only happens if uom is False
#            product_uom = product_obj.uom_id and product_obj.uom_id.id
#            product_uom_qty = qty_uos / product_obj.uos_coeff
#            th_weight = product_uom_qty * product_obj.weight
#        elif uom: # whether uos is set or not
#            default_uom = product_obj.uom_id and product_obj.uom_id.id
#            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
#            if product_obj.uos_id:
#                product_uos = product_obj.uos_id.id
#                product_uos_qty = qty * product_obj.uos_coeff
#            else:
#                product_uos = False
#                product_uos_qty =  qty
#                th_weight= q * product_obj.weight       # Round the quantity up
#    
#        if not uom2:
#            uom2 = product_obj.uom_id
#        if (product_obj.type=='product') and (product_obj.virtual_available * uom2.factor < qty * product_obj.uom_id.factor) \
#          and (product_obj.procure_method=='make_to_stock'):
#            res['warning'] = {
#                'title': _('Not enough stock !'),
#                'message': _('You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') %
#                    (qty, uom2 and uom2.name or product_obj.uom_id.name,
#                     max(0,product_obj.virtual_available), product_obj.uom_id.name,
#                     max(0,product_obj.qty_available), product_obj.uom_id.name)
#            }
#        # get unit price
#        if not pricelist:            
#            res['warning'] = {
#                'title': 'No Pricelist !',
#                'message':
#                    'You have to select a pricelist or a customer in the sales form !\n'
#                    'Please set one before choosing a product.'
#                }
#        else:
#            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
#                    product, qty or 1.0, partner_id, {
#                        'uom': uom,
#                        'date': date_order,
#                        })[pricelist]
#            if price is False:           
#                res['warning'] = {
#                    'title': 'No valid pricelist line found !',
#                    'message':
#                        "Couldn't find a pricelist line matching this product and quantity.\n"
#                        "You have to change either the product, the quantity or the pricelist."
#                    }
#            else:
#                price_unit = price
#                
#        res = {'value': {'product_uom_qty':product_uom_qty, 'product_packaging': product_packaging, 'delay': delay, 'tax_id': tax_id, 'type':type, 'name': name, 'product_uom': product_uom, 'product_uos': product_uos, 'product_uos_qty':product_uos_qty, 'th_weight': th_weight, 'price_unit': price_unit}}
#              
#        return res
    
    
    
    
    def _get_virtual_stock(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids):
            res[obj.id] = obj.product_id.virtual_available            
        return res
    
    def _get_real_stock(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids):
            res[obj.id] = obj.product_id.qty_available            
        return res
        
    _columns = {
        'virtual_avl': fields.function(_get_virtual_stock, method=True, string='Virtual Stock'),
        'qty_avl': fields.function(_get_real_stock, method=True, string='Real Stock'),
    }
sale_order_line()


class purchase_order_line(osv.osv):
    _inherit="purchase.order.line"
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=False, fiscal_position=False, date_planned=False,
            name=False, price_unit=False, notes=False):
#        if not pricelist:
#            raise osv.except_osv(_('No Pricelist !'), _('You have to select a pricelist or a supplier in the purchase form !\nPlease set one before choosing a product.'))
#        if not  partner_id:
#            raise osv.except_osv(_('No Partner!'), _('You have to select a partner in the purchase form !\nPlease set one partner before choosing a product.'))
        if not product:
            return {'value': {'price_unit': price_unit or 0.0, 'name': name or '',
                'notes': notes or'', 'product_uom' : uom or False}, 'domain':{'product_uom':[]}}
        res = {}
        prod= self.pool.get('product.product').browse(cr, uid, product)

        product_uom_pool = self.pool.get('product.uom')
        lang=False
        if partner_id:
            lang=self.pool.get('res.partner').read(cr, uid, partner_id, ['lang'])['lang']
        context={'lang':lang}
        context['partner_id'] = partner_id

        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        prod_uom_po = prod.uom_po_id.id
        if not uom:
            uom = prod_uom_po
        if not date_order:
            date_order = time.strftime('%Y-%m-%d')
        qty = qty or 1.0
        seller_delay = 0

        prod_name = self.pool.get('product.product').name_get(cr, uid, [prod.id], context=context)[0][1]
        res = {}
        for s in prod.seller_ids:
            if s.name.id == partner_id:
                seller_delay = s.delay
                if s.product_uom:
                    temp_qty = product_uom_pool._compute_qty(cr, uid, s.product_uom.id, s.min_qty, to_uom_id=prod.uom_id.id)
                    uom = s.product_uom.id #prod_uom_po
                temp_qty = s.min_qty # supplier _qty assigned to temp
                if qty < temp_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    qty = temp_qty
                    res.update({'warning': {'title': _('Warning'), 'message': _('The selected supplier has a minimal quantity set to %s, you cannot purchase less.') % qty}})
        qty_in_product_uom = product_uom_pool._compute_qty(cr, uid, uom, qty, to_uom_id=prod.uom_id.id)
        price = self.pool.get('product.pricelist').price_get(cr,uid,[pricelist],
                    product, qty_in_product_uom or 1.0, partner_id, {
                        'uom': uom,
                        'date': date_order,
                        })[pricelist]
        dt = (datetime.now() + relativedelta(days=int(seller_delay) or 0.0)).strftime('%Y-%m-%d %H:%M:%S')


        res.update({'value': {'price_unit': price, 'name': prod_name,
            'taxes_id':map(lambda x: x.id, prod.supplier_taxes_id),
            'date_planned': date_planned or dt,'notes': notes or prod.description_purchase,
            'product_qty': qty,
            'product_uom': uom}})
        domain = {}

        taxes = self.pool.get('account.tax').browse(cr, uid,map(lambda x: x.id, prod.supplier_taxes_id))
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        res['value']['taxes_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, taxes)

        res2 = self.pool.get('product.uom').read(cr, uid, [uom], ['category_id'])
        res3 = prod.uom_id.category_id.id
        domain = {'product_uom':[('category_id','=',res2[0]['category_id'][0])]}
        if res2[0]['category_id'][0] != res3:
            raise osv.except_osv(_('Wrong Product UOM !'), _('You have to select a product UOM in the same category than the purchase UOM of the product'))
        
        res['domain'] = domain       

        return res
    
    
purchase_order_line()
