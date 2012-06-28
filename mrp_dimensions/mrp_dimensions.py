# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
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

from osv import fields
from osv import osv
from tools import config

import netsvc
import time
from mx import DateTime
from tools.translate import _
import math
import decimal_precision as dp
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def name_serial(x, y, z, p, f, d):

     lote = '_'
     if (f == 'quadrangular'):
         lote = (str(x) + 'x' + str(y) + 'x' + str(z) + '_' + str(p))
     elif (f == 'cylindrical'):
         lote = (str(d) + 'x' + str(z) + '_' + str(p))

     return lote

def compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter):
       resu = {}
       
       weight = 0
       if shape == 'quadrangular':
           weight = ((size_x * size_y * size_z) * density * factor2 * (math.pow(factor3, 3))) / (factor1 * (math.pow(factor4, 3))) 
           diameter = 0
       elif shape == 'cylindrical':
               radius = diameter / 2.0
               weight = ((math.pow(radius, 2) * math.pi * size_z) * density * factor2 * (math.pow(factor3, 3))) / (factor1 * (math.pow(factor4, 3))) 
               size_x = 0
               size_y = 0
       else:
               weight = 0
               size_x = 0
               size_y = 0               
               size_z = 0

               
       resu = { 'weight':weight,
             'size_x':size_x,
             'size_y':size_y,
             'size_z':size_z,
             'diameter':diameter,
             'density':density,
             }
       return resu  




class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'size_x': fields.float('Width'),
        'size_y': fields.float('Length'),
        'size_z': fields.float('Thickness'),
        'density': fields.float('Density', help='Density unit= (uom of weight/(uom of size)^3)'),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape', help="Weight Formula for Quadrangular = width*length*thickness*density \n Weight Formula for Cylindrical= (diameter/2)^2*pi*thickness*density", required=True),
        'diameter' : fields.float('Diameter'),
        'purchase_price': fields.selection((('weight', 'Dimension'), ('units', 'Units')), 'Purchase price in', help="United of measure for purchase operations", required=True),
        'uom_d_size' : fields.many2one('product.uom', 'Size density cubic Uom', help="Default united of measure density used for operations size to cube", required=True),
        'uom_d_weight': fields.many2one('product.uom', 'Weight density Uom', help="Default united of measure density used for operations weight", required=True),
        'uom_s_size' : fields.many2one('product.uom', 'Size Uom', help="Default united of measure used for operations size", required=True),
        'prodlot_ids': fields.one2many('stock.production.lot', 'product_id', 'Production Lot List'),
    }
    _defaults = {
        'diameter': lambda * a: 0.0,
        'shape': lambda * a: 'other',
        'size_x': lambda * a: 0.0,
        'size_y': lambda * a: 0.0,
        'size_z': lambda * a: 0.0,
        'density': lambda * a: 0.0,
        'purchase_price': lambda * a: 'units',
        'uom_d_size' : lambda * a: 1,
        'uom_d_weight' : lambda * a: 1,
        'uom_s_size' : lambda * a: 1,
        }
    
    def compute_weight(self, cr, uid, id, uom_d_weight, uom_id, uom_d_size, uom_s_size, size_x, size_y, size_z, shape, density, diameter):
        res = {}
        if (not uom_id) or (not uom_d_weight) or(not uom_d_size) or (not uom_s_size):
            return 0
        if (shape):
           factor1 = self.pool.get('product.uom').browse(cr, uid, uom_d_weight, context='').factor
           factor2 = self.pool.get('product.uom').browse(cr, uid, uom_id, context='').factor
           factor3 = self.pool.get('product.uom').browse(cr, uid, uom_d_size, context='').factor
           factor4 = self.pool.get('product.uom').browse(cr, uid, uom_s_size, context='').factor                      
           res = compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)
           if shape == 'other':
               res.update({'purchase_price':'units'})
           return {'value': res}
product_product()        


class stock_production_lot(osv.osv):
    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'
    
    def _get_virtual_stock(self, cr, uid, ids, field_name, arg, context=None):
        """ Gets stock of products for locations
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        if 'location_id' not in context:
            locations = self.pool.get('stock.location').search(cr, uid, [('usage', '=', 'internal')], context=context)
        else:
            locations = context['location_id'] and [context['location_id']] or []

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}.fromkeys(ids, 0.0)
        if locations:
            cr.execute('''select
                    prodlot_id,
                    sum(qty)
                from
                    stock_report_prodlots_virtual
                where
                    location_id IN %s and prodlot_id IN %s group by prodlot_id''',(tuple(locations),tuple(ids),))
            res.update(dict(cr.fetchall()))

        return res 
    
    def _stock_virtual_search(self, cr, uid, obj, name, args, context=None):
        """ Searches Ids of products
        @return: Ids of locations
        """
        locations = self.pool.get('stock.location').search(cr, uid, [('usage', '=', 'internal')])
        cr.execute('''select
                prodlot_id,
                sum(qty)
            from
                stock_report_prodlots_virtual
            where
                location_id IN %s group by prodlot_id
            having  sum(qty) '''+ str(args[0][1]) + str(args[0][2]),(tuple(locations),))
        res = cr.fetchall()
        ids = [('id', 'in', map(lambda x: x[0], res))]
        return ids
    _columns = {
        'size_x': fields.float('Width'),
        'size_y': fields.float('Length'),
        'size_z': fields.float('Thickness'),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape', required=True),
        'diameter' : fields.float('Diameter'),
        'weight': fields.float('Dimension'),
        'density': fields.float('Density'),
        'virtual_stock': fields.function(_get_virtual_stock, fnct_search=_stock_virtual_search, method=True, type="float", string="Virtual", select=True,
            help="Current virtual quantity of products with this Production Lot Number in company warehouses",
            digits_compute=dp.get_precision('Product UoM')),
    }
    _defaults = {
        'diameter': lambda * a: 0.0,
        'shape': lambda * a: 'other',
        'size_x': lambda * a: 0.0,
        'size_y': lambda * a: 0.0,
        'size_z': lambda * a: 0.0,
        'weight': lambda * a: 0.0,
    }
    
    def generate_serial(self, cr, uid, ids, context={}):
       radio = 0
       for w in self.browse(cr, uid, ids):
           v = {
                'name' : name_serial(w.size_x, w.size_y, w.size_z, w.weight, w.shape, w.diameter)
                }
           w.write(v)
       return True
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor           
           res = compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)
           return {'value':res}
    
    
    def onchange_product_id(self, cr, uid, ids, product_id, context={}):
        if product_id:
            w = self.pool.get('product.product').browse(cr, uid, product_id, context)
            factor1 = w.uom_d_weight.factor
            factor2 = w.uom_id.factor
            factor3 = w.uom_d_size.factor
            factor4 = w.uom_s_size.factor                       
            v = {
                'size_x':w.size_x,
                'size_y':w.size_y,
                'size_z':w.size_z,
                'density':w.density,
                'shape':w.shape,
                'diameter':w.diameter,
                'weight':compute_w(cr, uid, factor1, factor2, factor3, factor4, w.size_x, w.size_y, w.size_z, w.shape, w.density, w.diameter)['weight']                                                                               
            }
            return {'value': v}
        return {}
stock_production_lot()    

class mrp_production_product_line(osv.osv):
    _name = 'mrp.production.product.line'    
    _inherit = 'mrp.production.product.line'
    _columns = { 
        'prodlot_id':fields.many2one('stock.production.lot', 'Lot'),
        'size_x': fields.float('Width'),
        'size_y': fields.float('Lenght'),
        'size_z': fields.float('Thickness'),
        'density': fields.float('Density'),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape'),
        'diameter' : fields.float('Diameter'),
        'weight': fields.float('Dimension')
                       
        }
    _defaults = {
        'shape': lambda * a: 'other',
         }


    def onchange_product_id(self, cr, uid, ids, product_id, context={}):
        if product_id:
            w = self.pool.get('product.product').browse(cr, uid, product_id, context)
            factor1 = w.uom_d_weight.factor
            factor2 = w.uom_id.factor
            factor3 = w.uom_d_size.factor
            factor4 = w.uom_s_size.factor                       
            v = {
                'product_uom':w.uom_id.id,
                'product_uos':w.uos_id and w.uos_id.id or w.uom_id.id,
                'size_x':w.size_x,
                'size_y':w.size_y,
                'size_z':w.size_z,
                'density':w.density,
                'shape':w.shape,
                'diameter':w.diameter,
                'weight':compute_w(cr, uid, factor1, factor2, factor3, factor4, w.size_x, w.size_y, w.size_z, w.shape, w.density, w.diameter)['weight']                                                                               
            }
            return {'value': v}
        return {}

    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
    
    
    
mrp_production_product_line()
   

class purchase_order(osv.osv):
    _name = "purchase.order"  
    _inherit = "purchase.order"    
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context):
        res = {}
        res = super(purchase_order, self)._amount_all(cr, uid, ids, field_name, arg, context) 
        cur_obj = self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:

                if line.purchase_price == 'weight':
                    product_qty = line.weight * line.product_qty
                else:
                    product_qty = line.product_qty
                for c in self.pool.get('account.tax').compute(cr, uid, line.taxes_id, line.price_unit, product_qty, order.partner_address_id.id, line.product_id, order.partner_id):
                    val += c['amount']
                val1 += line.price_subtotal
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res

    def _get_order(self, cr, uid, ids, context=None):
#        result = {}
        result = super(purchase_order, self)._get_order(cr, uid, ids, context) 
###        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
##            result[line.order_id.id] = True
        return result
 
    _columns = {
        'amount_untaxed': fields.function(_amount_all, method=True, string='Untaxed Amount',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums"),
        'amount_tax': fields.function(_amount_all, method=True, string='Taxes',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums"),
        'amount_total': fields.function(_amount_all, method=True, string='Total',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums"),
                }
    
    
    def action_picking_create(self, cr, uid, ids, *args):
        picking_id = False
        picking_id = super(purchase_order, self).action_picking_create(cr, uid, ids, *args)

        for order in self.browse(cr, uid, ids):
            for order_line in order.order_line:

                lote_id = False
                name_seriale = name_serial(order_line.size_x, order_line.size_y, order_line.size_z, order_line.weight, order_line.shape, order_line.diameter)

                datalote = {
                    'name':name_seriale,
                    'product_id': order_line.product_id.id,
                    'date' : order_line.date_planned,
                    'size_x' : order_line.size_x,
                    'size_y' : order_line.size_y,
                    'size_z' :order_line.size_z,
                    'shape' : order_line.shape,
                    'diameter' : order_line.diameter,
                    'density' : order_line.density,
                    'weight' : order_line.weight                                                                
                    }
                conditions = [('name','=',datalote['name']),('product_id','=',datalote['product_id']),('size_z','=',datalote['size_z']),('size_x','=',datalote['size_x']),('size_y','=',datalote['size_y']),('shape','=',datalote['shape']),('diameter','=',datalote['diameter']),('density','=',datalote['density'])]
                lot_list = self.pool.get('stock.production.lot').search(cr,uid,conditions)
                if lot_list:
                    lote_id = lot_list[0]
                else:
                    lote_id = self.pool.get('stock.production.lot').create(cr, uid, datalote)
                print lote_id
                production_line_orig = self.pool.get('mrp.production.product.line').search(cr, uid,
                    [('production_id', '=', order_line.production_id.id),
                     ('product_id', '=', order_line.product_id.id),
                     ('size_x', '=', order_line.size_x),
                     ('size_y', '=', order_line.size_y),
                     ('shape', '=', order_line.shape)])
                if production_line_orig and production_line_orig[0] :
                    product_line_orig = self.pool.get('mrp.production.product.line').browse(cr, uid, production_line_orig[0])
                    name_seriale = name_serial(product_line_orig.size_x, product_line_orig.size_y, product_line_orig.size_z, product_line_orig.weight, product_line_orig.shape, product_line_orig.diameter)
                    l = self.pool.get('stock.production.lot').search(cr, uid, [('product_id', '=', product_line_orig.product_id.id), ('name', '=', name_seriale)])
                    if not l:
                            datalote = {
                                'name':name_seriale,
                                'product_id': product_line_orig.product_id.id,
                                'date' : production.date_planned,
                                'size_x' : product_line_orig.size_x,
                                'size_y' : product_line_orig.size_y,
                                'size_z' : product_line_orig.size_z,
                                'shape' : product_line_orig.shape,
                                'diameter' : product_line_orig.diameter,
                                'density' : product_line_orig.density,
                                'weight' : product_line_orig.weight                                                                
                                }
                            lote_id = self.pool.get('stock.production.lot').create(cr, uid, datalote)
                    else:
                        lote_id = l[0]

                if not order_line.product_id:
                    continue
                if order_line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    stock_move_id = self.pool.get('stock.move').search(cr, uid, [('purchase_line_id', '=', order_line.id)])
                    if stock_move_id:
                        self.pool.get('stock.move').write(cr, uid, stock_move_id, {'prodlot_id':lote_id})                                                                                    
        return picking_id


purchase_order()


class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    
    def _amount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        res = super(purchase_order_line, self)._amount_line(cr, uid, ids, prop, unknow_none, unknow_dict)        
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            cur = line.order_id.pricelist_id.currency_id
            if line.purchase_price == 'weight':
                product_qty = line.weight * line.product_qty
            else:
                product_qty = line.product_qty
            res[line.id] = cur_obj.round(cr, uid, cur, line.price_unit * product_qty)
        return res
    

    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=False, fiscal_position=False, date_planned=False,
            name=False, price_unit=False, notes=False):
        result = super(purchase_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=False, fiscal_position=False, date_planned=False,
            name=False, price_unit=False, notes=False)
        if not product:
            return result
        for product_obj in self.pool.get('product.product').browse(cr, uid, [product]):
            result['value']['purchase_price'] = product_obj.purchase_price
            result['value']['shape'] = product_obj.shape
            result['value']['size_x'] = product_obj.size_x
            result['value']['size_y'] = product_obj.size_y
            result['value']['size_z'] = product_obj.size_z
            result['value']['density'] = product_obj.density
            result['value']['diameter'] = product_obj.diameter
            result['value']['weight'] = compute_w(cr, uid, product_obj.uom_d_weight.factor, product_obj.uom_id.factor, product_obj.uom_d_size.factor, product_obj.uom_s_size.factor, product_obj.size_x, product_obj.size_y, product_obj.size_z, product_obj.shape, product_obj.density, product_obj.diameter)['weight']        

        return result
    
    _columns = {
        'production_id': fields.many2one('mrp.production', 'Produccion', readonly=True),
        'size_x': fields.float('Width',),
        'size_y': fields.float('Length',),
        'size_z': fields.float('Thickness',),
        'density': fields.float('Density',),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape'),
        'diameter' : fields.float('Diameter',),
        'weight': fields.float('Dimension',),
        'purchase_price': fields.selection((('weight', 'Dimension'), ('units', 'Units')), 'Price in'),
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal'),
    }
    _defaults = {
        'shape': lambda * a: 'other',
        'purchase_price': lambda * a: 'units',
         }
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
       
purchase_order_line()

class sale_order_line(osv.osv):
    _name = "sale.order.line"
    _inherit = "sale.order.line"
    
    
    def  _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        res = super(sale_order_line, self)._amount_line(cr, uid, ids, field_name, arg, context=None)        
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            cur = line.order_id.pricelist_id.currency_id
            product_uom_qty = line.product_uom_qty
            if line.sale_price == 'weight':
                product_uom_qty = line.weight * line.product_uom_qty
            res[line.id] = cur_obj.round(cr, uid, cur, line.price_unit * product_uom_qty)
        return res

    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        result = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag)
        if not product:
            return result
        for product_obj in self.pool.get('product.product').browse(cr, uid, [product]):
            result['value']['sale_price'] = product_obj.purchase_price
            result['value']['shape'] = product_obj.shape
            result['value']['size_x'] = product_obj.size_x
            result['value']['size_y'] = product_obj.size_y
            result['value']['size_z'] = product_obj.size_z
            result['value']['density'] = product_obj.density
            result['value']['diameter'] = product_obj.diameter
            result['value']['weight'] = compute_w(cr, uid, product_obj.uom_d_weight.factor, product_obj.uom_id.factor, product_obj.uom_d_size.factor, product_obj.uom_s_size.factor, product_obj.size_x, product_obj.size_y, product_obj.size_z, product_obj.shape, product_obj.density, product_obj.diameter)['weight']        

        return result
    
    _columns = {
        'production_id': fields.many2one('mrp.production', 'Produccion', readonly=True),
        'size_x': fields.float('Width',),
        'size_y': fields.float('Length',),
        'size_z': fields.float('Thickness',),
        'density': fields.float('Density',),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape', required=True,),
        'diameter' : fields.float('Diameter',),
        'weight': fields.float('Dimension',),
        'sale_price': fields.selection((('weight', 'Dimension'), ('units', 'Units')), 'Price in', required=True),
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal'),
    }
    _defaults = {
        'shape': lambda * a: 'other',
        'sale_price': lambda * a: 'units',
         }
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
       res={}
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor    
           res=compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)
           return {'value':res }
       
sale_order_line()



#===============================================================================
# ABASTECIMIENTOS AUTOMÁTICOS(PRODUCIR)
#===============================================================================



class mrp_maker(osv.osv):
    
    _name='mrp.maker'
   
    _columns = {
                'color_id': fields.char('Color HTML', size=7),
                'product_id':fields.many2one('product.product', 'Product', required=True),
                'product_qty':fields.float('Quantity', required=True, digits=(16,2)),
                'product_uom': fields.many2one('product.uom', 'Product UoM', required=True),
                'size_x': fields.float('Width'),
                'size_y': fields.float('Length'),
                'size_z': fields.float('Thickness'),
                'density': fields.float('Density'),
                'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape'),
                'diameter' : fields.float('Diameter'),
                'weight': fields.float('Dimension'),
                'line_ids':fields.one2many('mrp.maker.line','maker_id', 'Lines'),
                'final_line_ids':fields.one2many('mrp.maker.final.line','maker_id', 'Final Lines'),
                'sale_line':fields.many2one('sale.order.line', 'Sale line'),
                }    
    
    
    _defaults = {
        'diameter': lambda * a: 0.0,
        'shape': lambda * a: 'other',
        'size_x': lambda * a: 0.0,
        'size_y': lambda * a: 0.0,
        'size_z': lambda * a: 0.0,
        'weight': lambda * a: 0.0,
        'density': lambda * a: 0.0,
    }
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        result = []
        
        for line in self.browse(cr, uid, ids, context=context):
            name=""
            name += line.product_id.name + ' : ' + line.shape
            if line.shape == 'quadrangular':
                name += ' : ' + str(line.density) + '_' + str(line.size_x) + 'x' + str(line.size_y) + 'x' + str(line.size_z)
            elif line.shape == 'cylindrical':
                name += ' : ' + str(line.density) + '_' + str(line.size_z) + 'x' + str(line.diameter)
            result.append((line.id, name))
        return result
        
        
        
        
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
        if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor  
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
    
    
    def product_id_change(self, cr, uid, ids, product, context=None):
        res = {}
        if not product:
            return res
        for product_obj in self.pool.get('product.product').browse(cr, uid, [product]):
            res.update({'shape': product_obj.shape,'size_x': product_obj.size_x,'size_y': product_obj.size_y,'size_z': product_obj.size_z,'density': product_obj.density, 'diameter': product_obj.diameter,'weight': compute_w(cr, uid, product_obj.uom_d_weight.factor, product_obj.uom_id.factor, product_obj.uom_d_size.factor, product_obj.uom_s_size.factor, product_obj.size_x, product_obj.size_y, product_obj.size_z, product_obj.shape, product_obj.density, product_obj.diameter)['weight'],'product_uom': product_obj.uom_id.id}) 
        return {'value': res}
    
mrp_maker()

class mrp_maker_line(osv.osv):
    
    _name='mrp.maker.line'
    
    _columns = {
                'product_id':fields.many2one('product.product', 'Product', required=True),
                'product_qty':fields.float('Quantity', required=True, digits=(16,2)),
                'product_uom': fields.many2one('product.uom', 'Product UoM', required=True),
                'size_x': fields.float('Width'),
                'size_y': fields.float('Length'),
                'size_z': fields.float('Thickness'),
                'density': fields.float('Density'),
                'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape'),
                'diameter' : fields.float('Diameter'),
                'weight': fields.float('Dimension'),
                'maker_id':fields.many2one('mrp.maker', 'Parent'),
                }   
    
    
    _defaults = {
        'diameter': lambda * a: 0.0,
        'shape': lambda * a: 'other',
        'size_x': lambda * a: 0.0,
        'size_y': lambda * a: 0.0,
        'size_z': lambda * a: 0.0,
        'weight': lambda * a: 0.0,
        'density': lambda * a: 0.0,
    }
    
    def product_id_change(self, cr, uid, ids, product, context=None):
        res = {}
        if not product:
            return res
        for product_obj in self.pool.get('product.product').browse(cr, uid, [product]):
            res.update({'shape': product_obj.shape,'size_x': product_obj.size_x,'size_y': product_obj.size_y,'size_z': product_obj.size_z,'density': product_obj.density, 'diameter': product_obj.diameter,'weight': compute_w(cr, uid, product_obj.uom_d_weight.factor, product_obj.uom_id.factor, product_obj.uom_d_size.factor, product_obj.uom_s_size.factor, product_obj.size_x, product_obj.size_y, product_obj.size_z, product_obj.shape, product_obj.density, product_obj.diameter)['weight'],'product_uom': product_obj.uom_id.id}) 
        return {'value': res}
    
    
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
        if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor  
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
mrp_maker_line()
class mrp_maker_final_line(osv.osv):
    
    _name='mrp.maker.final.line'
    
    _columns = {
                'product_id':fields.many2one('product.product', 'Product', required=True),
                'product_qty':fields.float('Quantity', required=True, digits=(16,2)),
                'product_uom': fields.many2one('product.uom', 'Product UoM', required=True),
                'size_x': fields.float('Width'),
                'size_y': fields.float('Length'),
                'size_z': fields.float('Thickness'),
                'density': fields.float('Density'),
                'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape'),
                'diameter' : fields.float('Diameter'),
                'weight': fields.float('Dimension'),
                'maker_id':fields.many2one('mrp.maker', 'Parent'),
                }   
    
    
    _defaults = {
        'diameter': lambda * a: 0.0,
        'shape': lambda * a: 'other',
        'size_x': lambda * a: 0.0,
        'size_y': lambda * a: 0.0,
        'size_z': lambda * a: 0.0,
        'weight': lambda * a: 0.0,
        'density': lambda * a: 0.0,
    }
    
    def product_id_change(self, cr, uid, ids, product, context=None):
        res = {}
        if not product:
            return res
        for product_obj in self.pool.get('product.product').browse(cr, uid, [product]):
            res.update({'shape': product_obj.shape,'size_x': product_obj.size_x,'size_y': product_obj.size_y,'size_z': product_obj.size_z,'density': product_obj.density, 'diameter': product_obj.diameter,'weight': compute_w(cr, uid, product_obj.uom_d_weight.factor, product_obj.uom_id.factor, product_obj.uom_d_size.factor, product_obj.uom_s_size.factor, product_obj.size_x, product_obj.size_y, product_obj.size_z, product_obj.shape, product_obj.density, product_obj.diameter)['weight'],'product_uom': product_obj.uom_id.id}) 
        return {'value': res}
    
    
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
        if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor  
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
mrp_maker_final_line()
 
class mrp_production(osv.osv):
    _name = 'mrp.production'
    _description = 'Production'
    _inherit = 'mrp.production'    
    _columns = { 
        'product_line_origin': fields.many2one('mrp.production.product.line', 'Linea de produccion original'),
        'size_x': fields.float('Width'),
        'size_y': fields.float('Length'),
        'size_z': fields.float('Thickness'),
        'density': fields.float('Density'),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape'),
        'diameter' : fields.float('Diameter'),
        'weight': fields.float('Dimension'),
        'maker': fields.many2one('mrp.maker', 'Config', readonly=True),
        }

        
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
        if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor  
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
   
    def onchange_product_id(self, cr, uid, ids, product_id, context={}):
        if product_id:
            w = self.pool.get('product.product').browse(cr, uid, [product_id], context)[0]
            factor1 = w.uom_d_weight.factor
            factor2 = w.uom_id.factor
            factor3 = w.uom_d_size.factor
            factor4 = w.uom_s_size.factor   
            bom_o = False  
            bom = self.pool.get('mrp.bom').search(cr,uid,[('product_id', '=', product_id)])   
            if bom:
                bom_o = bom[0]    
            v = {
                'product_uom':w.uom_id.id,
                'product_uos':w.uos_id and w.uos_id.id or w.uom_id.id,
                'size_x':w.size_x,
                'size_y':w.size_y,
                'size_z':w.size_z,
                'density':w.density,
                'shape':w.shape,
                'diameter':w.diameter,
                'weight': compute_w(cr, uid, factor1, factor2, factor3, factor4, w.size_x, w.size_y, w.size_z, w.shape, w.density, w.diameter)['weight'],
                'name' : w.name,
                'bom_id':bom_o,  
            }
            return {'value': v}
        return {}  

    def action_confirm(self, cr, uid, ids):
        """ Confirms production order.
        @return: Newly generated picking Id.
        """
        picking_id = False
        proc_ids = []
        seq_obj = self.pool.get('ir.sequence')
        pick_obj = self.pool.get('stock.picking')
        move_obj = self.pool.get('stock.move')
        proc_obj = self.pool.get('procurement.order')
        lot_obj = self.pool.get('stock.production.lot')
        wf_service = netsvc.LocalService("workflow")
        for production in self.browse(cr, uid, ids):
            if not production.product_lines:
                self.action_compute(cr, uid, [production.id])
                production = self.browse(cr, uid, [production.id])[0]
            routing_loc = None
            pick_type = 'internal'
            address_id = False
            if production.bom_id.routing_id and production.bom_id.routing_id.location_id:
                routing_loc = production.bom_id.routing_id.location_id
                if routing_loc.usage <> 'internal':
                    pick_type = 'out'
                address_id = routing_loc.address_id and routing_loc.address_id.id or False
                routing_loc = routing_loc.id
            pick_name = seq_obj.get(cr, uid, 'stock.picking.' + pick_type)
            picking_id = pick_obj.create(cr, uid, {
                'name': pick_name,
                'origin': (production.origin or '').split(':')[0] + ':' + production.name,
                'type': pick_type,
                'move_type': 'one',
                'state': 'auto',
                'address_id': address_id,
                'auto_picking': self._get_auto_picking(cr, uid, production),
                'company_id': production.company_id.id,
            })

            source = production.product_id.product_tmpl_id.property_stock_production.id
            final_lot=False
            if production.shape in ('quadrangular', 'cylindrical'):
                final_lot_domain = [('product_id', '=', production.product_id.id),('shape', '=', production.shape),('size_x', '=', production.size_x),('size_y', '=', production.size_y),('size_z','=', production.size_z),('diameter', '=', production.diameter),('weight', '=', production.weight),('density', '=', production.density)]
                final_lot_dict = {
                           'product_id':production.product_id.id,
                           'shape':production.shape,
                           'size_x':production.size_x,
                           'size_y':production.size_y,
                           'size_z':production.size_z,
                           'diameter':production.diameter,
                           'weight':production.weight,
                           'density':production.density,
                           }
            
                final_lot_list = lot_obj.search(cr,uid,final_lot_domain)
                if final_lot_list:
                    final_lot = final_lot_list[0]
                else:
                    final_lot = lot_obj.create(cr,uid,final_lot_dict)
                    lot_obj.generate_serial(cr,uid,[final_lot])
            
            data = {
                'name':'PROD:' + production.name,
                'date': production.date_planned,
                'product_id': production.product_id.id,
                'product_qty': production.product_qty,
                'product_uom': production.product_uom.id,
                'product_uos_qty': production.product_uos and production.product_uos_qty or False,
                'product_uos': production.product_uos and production.product_uos.id or False,
                'location_id': source,
                'location_dest_id': production.location_dest_id.id,
                'move_dest_id': production.move_prod_id.id,
                'state': 'waiting',
                'company_id': production.company_id.id,
            }
            if final_lot:
                data['prodlot_id']=final_lot
            res_list = []
            res_final_id = move_obj.create(cr, uid, data)
            res_list.append(res_final_id)
            for line_id in production.move_created_ids:
                res_list.append(line_id.id)
            self.write(cr, uid, [production.id], {'move_created_ids': [(6, 0, res_list)]})
            moves = []
            for line in production.product_lines:
                move_id = False
                prodlot_id = False
                if line.prodlot_id:
                    prodlot_id = line.prodlot_id.id
                elif line.shape in ('quadrangular', 'cylindrical'):
                    lot_domain = [('product_id', '=', line.product_id.id),('shape', '=', line.shape),('size_x', '=', line.size_x),('size_y', '=', line.size_y),('size_z','=', line.size_z),('diameter', '=', line.diameter),('weight', '=', line.weight),('density', '=', line.density)]
                    lot_dict = {
                       'product_id':line.product_id.id,
                       'shape':line.shape,
                       'size_x':line.size_x,
                       'size_y':line.size_y,
                       'size_z':line.size_z,
                       'diameter':line.diameter,
                       'weight':line.weight,
                       'density':line.density,
                       }
                    lot_list = lot_obj.search(cr,uid,lot_domain)
                    if lot_list:
                        prodlot_id = lot_list[0]
                    else:
                        prodlot_id = lot_obj.create(cr,uid,lot_dict)
                        lot_obj.generate_serial(cr,uid,[prodlot_id])
                newdate = production.date_planned
                if line.product_id.type in ('product', 'consu'):
                    res_dest_id = move_obj.create(cr, uid, {
                        'name':'PROD:' + production.name,
                        'date': production.date_planned,
                        'product_id': line.product_id.id,
                        'prodlot_id': prodlot_id,
                        'product_qty': line.product_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': line.product_uos and line.product_uos_qty or False,
                        'product_uos': line.product_uos and line.product_uos.id or False,
                        'location_id': routing_loc or production.location_src_id.id,
                        'location_dest_id': source,
                        'move_dest_id': res_final_id,
                        'state': 'waiting',
                        'company_id': production.company_id.id,
                    })
                    moves.append(res_dest_id)
                    move_id = move_obj.create(cr, uid, {
                        'name':'PROD:' + production.name,
                        'picking_id':picking_id,
                        'product_id': line.product_id.id,
                        'prodlot_id':prodlot_id,
                        'product_qty': line.product_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': line.product_uos and line.product_uos_qty or False,
                        'product_uos': line.product_uos and line.product_uos.id or False,
                        'date': newdate,
                        'move_dest_id': res_dest_id,
                        'location_id': production.location_src_id.id,
                        'location_dest_id': routing_loc or production.location_src_id.id,
                        'state': 'waiting',
                        'company_id': production.company_id.id,
                    })
                proc_id = proc_obj.create(cr, uid, {
                    'name': (production.origin or '').split(':')[0] + ':' + production.name,
                    'origin': (production.origin or '').split(':')[0] + ':' + production.name,
                    'date_planned': newdate,
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    'product_uom': line.product_uom.id,
                    'product_uos_qty': line.product_uos and line.product_qty or False,
                    'product_uos': line.product_uos and line.product_uos.id or False,
                    'location_id': production.location_src_id.id,
                    'procure_method': line.product_id.procure_method,
                    'move_id': move_id,
                    'company_id': production.company_id.id,
                    'size_x':line.size_x,
                    'size_y':line.size_y,
                    'size_z':line.size_z,
                    'shape':line.shape,
                    'diameter':line.diameter,
                    'weight':line.weight,
                    'density':line.density,
                    'price_type':line.product_id.purchase_price,
                })
                wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)
                proc_ids.append(proc_id)
            wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
            self.write(cr, uid, [production.id], {'picking_id': picking_id, 'move_lines': [(6,0,moves)], 'state':'confirmed'})
            message = _("Manufacturing order '%s' is scheduled for the %s.") % (
                production.name,
                datetime.strptime(production.date_planned,'%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'),
            )
            self.log(cr, uid, production.id, message)
        return picking_id




    def action_compute(self, cr, uid, ids, properties=[]):
        """ Computes bills of material of a product.
        @param properties: List containing dictionaries of properties.
        @return: No. of products.
        """
        results = []
        bom_obj = self.pool.get('mrp.bom')
        uom_obj = self.pool.get('product.uom')
        prod_line_obj = self.pool.get('mrp.production.product.line')
        workcenter_line_obj = self.pool.get('mrp.production.workcenter.line')
        for production in self.browse(cr, uid, ids):
            cr.execute('delete from mrp_production_product_line where production_id=%s', (production.id,))
            cr.execute('delete from mrp_production_workcenter_line where production_id=%s', (production.id,))
            bom_point = production.bom_id
            bom_id = production.bom_id.id
            if not bom_point:
                bom_id = bom_obj._bom_find(cr, uid, production.product_id.id, production.product_uom.id, properties)
                if bom_id:
                    bom_point = bom_obj.browse(cr, uid, bom_id)
                    routing_id = bom_point.routing_id.id or False
                    self.write(cr, uid, [production.id], {'bom_id': bom_id, 'routing_id': routing_id})

            if not bom_id:
                raise osv.except_osv(_('Error'), _("Couldn't find bill of material for product"))

            factor = uom_obj._compute_qty(cr, uid, production.product_uom.id, production.product_qty, bom_point.product_uom.id)
            res = bom_obj._bom_explode(cr, uid, bom_point, factor / bom_point.product_qty, properties)
            results = res[0]
            results2 = res[1]
            for line in results:
                line['production_id'] = production.id
                prod_line_obj.create(cr, uid, line)
            for line in results2:
                line['production_id'] = production.id
                workcenter_line_obj.create(cr, uid, line)
        return len(results) 
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'maker': False
        })
        return super(mrp_production, self).copy(cr, uid, id, default, context)
mrp_production() 