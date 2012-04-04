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
        'purchase_price': fields.selection((('weight', 'Weight'), ('units', 'Units')), 'Purchase price in', help="United of measure for purchase operations", required=True),
        'uom_d_size' : fields.many2one('product.uom', 'Size density cubic Uom', help="Default united of measure density used for operations size to cube", required=True),
        'uom_d_weight': fields.many2one('product.uom', 'Weight density Uom', help="Default united of measure density used for operations weight", required=True),
        'uom_s_size' : fields.many2one('product.uom', 'Size Uom', help="Default united of measure used for operations size", required=True),
        
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
        'weight': fields.float('Weight'),
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

    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter):
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
    
    
 
stock_production_lot()    

class mrp_production_product_line(osv.osv):
    _name = 'mrp.production.product.line'    
    _inherit = 'mrp.production.product.line'
    _columns = { 
        'size_x': fields.float('Width'),
        'size_y': fields.float('Lenght'),
        'size_z': fields.float('Thickness'),
        'density': fields.float('Density'),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape'),
        'diameter' : fields.float('Diameter'),
        'weight': fields.float('Weight')
                       
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
        'weight': fields.float('Weight'),
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
            }
            if ids :
                v['bom_id'] = ids[0]
            return {'value': v}
        return {}  

    def action_compute(self, cr, uid, ids, properties=[]):
        results = []

        result = super(mrp_production, self).action_compute(cr, uid, ids, properties)
        
        for production in self.browse(cr, uid, ids):
            i = 0
            bom_id = production.bom_id.id
            for a in self.pool.get('mrp.production.product.line').search(cr, uid, [('production_id', '=', production.id)]):
                production_line = self.pool.get('mrp.production.product.line').browse(cr, uid, a)
                w = False
                w2 = False
#                if not (production.product_line_origin):
#                    p = self.pool.get('mrp.bom').browse(cr, uid, bom_id)
#                    w = self.pool.get('mrp.bom').browse(cr, uid, p.bom_lines[i].id)
#                    if w:
#                        v = {                        
#                            'product_uom':w.product_uom.id,
#                            'product_uos':w.product_uos and w.product_uos.id or w.product_uom.id,
#                            'size_x':w.size_x,
#                            'size_y':w.size_y,
#                            'size_z':w.size_z,
#                            'density':w.density,
##                            'shape':w.shape,
#                            'diameter':w.diameter,
#                            'weight':w.weight                                                                               
#                            }
#                else:
#                    origen = production.origin[1:]
#
#                    w2 = self.pool.get('mrp.production.product.line').browse(cr, uid, production.product_line_origin.id)
#                    v = {
#                        'size_x':w2.size_x,
#                        'size_y':w2.size_y,
#                        'size_z':w2.size_z,
#                        'density':w2.density,
##                        'shape':w2.shape,
#                        'diameter':w2.diameter,
#                        'weight':w2.weight                                                                               
#                    }
#                if (w or w2):
#                    production_line.write(v)
                i = i + 1
                
        return len(results)       

    def action_confirm(self, cr, uid, ids):
   
        picking_id = super(mrp_production, self).action_confirm(cr, uid, ids)
        for production in self.browse(cr, uid, ids):     
            stock_move_id = False
            lote_id = False
            routing_loc = None
            pick_type = 'internal'
            address_id = False            
            if production.bom_id.routing_id and production.bom_id.routing_id.location_id:
                routing_loc = production.bom_id.routing_id.location_id
                if routing_loc.usage <> 'internal':
                    pick_type = 'out'
                address_id = routing_loc.address_id and routing_loc.address_id.id or False
                routing_loc = routing_loc.id

            
            if (production.product_line_origin and production.product_line_origin.id):
                product_line_orig = self.pool.get('mrp.production.product.line').browse(cr, uid, production.product_line_origin.id)

                name_seriale = name_serial(product_line_orig.size_x, product_line_orig.size_y, product_line_orig.size_z, product_line_orig.weight, product_line_orig.shape, product_line_orig.diameter)
                l = self.pool.get('stock.production.lot').search(cr, uid, [('product_id', '=', product_line_orig.product_id.id), ('name', '=', name_seriale)])
                if not l:
                        datalote = {
                            'name':name_seriale,
                            'product_id': product_line_orig.product_id.id,
                            'date' : production.date_planned
                            }
                        lote_id = self.pool.get('stock.production.lot').create(cr, uid, datalote)
                else:
                    lote_id = l[0]
            source = production.product_id.product_tmpl_id.property_stock_production.id   
            stock_move_id = self.pool.get('stock.move').search(cr, uid, [('name', '=', 'PROD:' + production.name),
                                                                       ('product_id', '=', production.product_id.id),
                                                                       ('location_id', '=', source),
                                                                       ('location_dest_id', '=', production.location_dest_id.id),
                                                                       ('move_dest_id', '=', production.move_prod_id.id)])
            if (stock_move_id and stock_move_id[0]):
                self.pool.get('stock.move').write(cr, uid, stock_move_id[0], {'prodlot_id': lote_id or False})                                        

            products = {}
           
            for line in production.product_lines:
                mrp_producurement_id = None
                if products.has_key(line.product_id.id):
                    products[line.product_id.id] = products[line.product_id.id] + 1
                else: 
                    products[line.product_id.id] = 0                     

                stock_move_id2 = False
                stock_move_id3 = False               
                name_seriale = name_serial(line.size_x, line.size_y, line.size_z, line.weight, line.shape, line.diameter)
                l = self.pool.get('stock.production.lot').search(cr, uid, [('product_id', '=', line.product_id.id), ('name', '=', name_seriale)])
                if not l:
                        datalote = {
                            'name':name_seriale,
                            'product_id': line.product_id.id,
                            'date' : production.date_planned,
                            'size_x' : line.size_x,
                            'size_y' : line.size_y,
                            'size_z' : line.size_z,
                            'shape' : line.shape,
                            'diameter' : line.diameter,
                            'density' : line.density,
                            'weight' : line.weight,
                            
                            }
                        lote_id2 = self.pool.get('stock.production.lot').create(cr, uid, datalote)
                else:
                    lote_id2 = l[0]

                if line.product_id.type in ('product', 'consu'):                
                    stock_move_id2 = self.pool.get('stock.move').search(cr, uid, [('name', '=', 'PROD:' + production.name),
                                                                       ('product_id', '=', line.product_id.id),
                                                                       ('location_id', '=', routing_loc or production.location_src_id.id),
                                                                       ('location_dest_id', '=', source),
                                                                       ('move_dest_id', '=', stock_move_id),
                                                                       ('product_qty', '=', line.product_qty)])
                    if (stock_move_id2 and stock_move_id2[products[line.product_id.id]]):
                        self.pool.get('stock.move').write(cr, uid, stock_move_id2[products[line.product_id.id]], {'prodlot_id': lote_id2 or False})


            
                    stock_move_id3 = self.pool.get('stock.move').search(cr, uid, [('name', '=', 'PROD:' + production.name),
                                                                       ('product_id', '=', line.product_id.id),
                                                                       ('location_id', '=', production.location_src_id.id),
                                                                       ('location_dest_id', '=', routing_loc or production.location_src_id.id),
                                                                       ('move_dest_id', '=', stock_move_id2[products[line.product_id.id]])])
                    if (stock_move_id3 and stock_move_id3[0]):
                        self.pool.get('stock.move').write(cr, uid, stock_move_id3[0], {'prodlot_id': lote_id2 or False})
                if (stock_move_id3 and stock_move_id3[0]):
                    mrp_procurement_id = self.pool.get('procurement.order').search(cr, uid, [('move_id', '=', stock_move_id3[0])])
                    self.pool.get('procurement.order').write(cr, uid, mrp_procurement_id, {'product_line_origin' : line.id})
                    origin = (production.origin or '') + ':' + production.name
                    mrp_production_id = self.pool.get('mrp.production').search(cr, uid, [('origin', '=', origin), ('product_id', '=', line.product_id.id)]) 
                    mrp_production_id.sort()

                    data = {
                            'size_x' : line.size_x,
                            'size_y' : line.size_y,
                            'size_z' : line.size_z,
                            'shape' : line.shape,
                            'diameter' : line.diameter,
                            'density' : line.density,
                            'weight' : line.weight,
                            }

                    if mrp_production_id:
                        self.pool.get('mrp.production').write(cr, uid, mrp_production_id[products[line.product_id.id]], {'product_line_origin' : line.id})
                        production_product_id = self.pool.get('mrp.production.product.line').search(cr, uid, [('production_id', '=', mrp_production_id[products[line.product_id.id]])])
                        self.pool.get('mrp.production.product.line').write(cr, uid, production_product_id, data)
                    else:
                        if production.product_line_origin:
                            data = {
                            'size_x' : production.product_line_origin.size_x,
                            'size_y' : production.product_line_origin.size_y,
                            'size_z' : production.product_line_origin.size_z,
                            'shape' : production.product_line_origin.shape,
                            'diameter' : production.product_line_origin.diameter,
                            'density' : production.product_line_origin.density,
                            'weight' : production.product_line_origin.weight,
                            }
                            
                        for purchase in self.pool.get('purchase.order.line').search(cr, uid, [('production_id', '=', production.id)]):
                                self.pool.get('purchase.order.line').write(cr, uid, purchase, data)                        
                        
        return picking_id

mrp_production() 
 
 
 
 
class sale_order(osv.osv):
    _name = "sale.order"  
    _inherit = "sale.order" 
	
    def action_ship_create(self, cr, uid, ids, *args):
        lot_object = self.pool.get('stock.production.lot')         
        wf_service = netsvc.LocalService("workflow")
        picking_id = False
        move_obj = self.pool.get('stock.move')
        proc_obj = self.pool.get('procurement.order')
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id
        for order in self.browse(cr, uid, ids, context={}):
            proc_ids = []
            output_id = order.shop_id.warehouse_id.lot_output_id.id
            picking_id = False
            for line in order.order_line:
                proc_id = False
                date_planned = datetime.now() + relativedelta(days=line.delay or 0.0)
                date_planned = (date_planned - timedelta(days=company.security_lead)).strftime('%Y-%m-%d %H:%M:%S')
                lote_id = False
                lot_ids = lot_object.search(cr, uid, 
                    [('product_id', '=', line.product_id.id),
                     ('size_x', '=', line.size_x),
                     ('size_y', '=', line.size_y),
                     ('size_z', '=', line.size_z),
                     ('diameter', '=', line.diameter),
                     ('weight', '=', line.weight),                     
                     ('shape', '=', line.shape)])
                if not lot_ids:                
                    name_seriale = name_serial(line.size_x, line.size_y, line.size_z, line.weight, line.shape, line.diameter)
                    datalote = {
                        'name':name_seriale,
                        'product_id': line.product_id.id,
                        'date' : time.strftime('%Y-%m-%d'),
                        'size_x' : line.size_x,
                        'size_y' : line.size_y,
                        'size_z' :line.size_z,
                        'shape' : line.shape,
                        'diameter' : line.diameter,
                        'density' : line.density,
                        'weight' : line.weight                                                                
                        }
                    lote_id = lot_object.create(cr, uid, datalote)
                else:
                    lote_id = lot_ids[0]
                
                
                if line.state == 'done':
                    continue
                move_id = False
                if line.product_id and line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    location_id = order.shop_id.warehouse_id.lot_stock_id.id
                    if not picking_id:
                        pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.out')
                        picking_id = self.pool.get('stock.picking').create(cr, uid, {
                            'name': pick_name,
                            'origin': order.name,
                            'type': 'out',
                            'state': 'auto',
                            'move_type': order.picking_policy,
                            'sale_id': order.id,
                            'address_id': order.partner_shipping_id.id,
                            'note': order.note,
                            'invoice_state': (order.order_policy=='picking' and '2binvoiced') or 'none',
                            'company_id': order.company_id.id,
                        })
                    move_id = self.pool.get('stock.move').create(cr, uid, {
                        'name': line.name[:64],
                        'picking_id': picking_id,
                        'product_id': line.product_id.id,
                        'date': date_planned,
                        'date_expected': date_planned,
                        'product_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': line.product_uos_qty,
                        'product_uos': (line.product_uos and line.product_uos.id)\
                                or line.product_uom.id,
                        'product_packaging': line.product_packaging.id,
                        'address_id': line.address_allotment_id.id or order.partner_shipping_id.id,
                        'location_id': location_id,
                        'location_dest_id': output_id,
                        'sale_line_id': line.id,
                        'tracking_id': False,
                        'prodlot_id':lote_id,
                        'state': 'draft',
                        #'state': 'waiting',
                        'note': line.notes,
                        'company_id': order.company_id.id,
                    })

                if line.product_id:
                    proc_id = self.pool.get('procurement.order').create(cr, uid, {
                        'name': line.name,
                        'origin': order.name,
                        'date_planned': date_planned,
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': (line.product_uos and line.product_uos_qty)\
                                or line.product_uom_qty,
                        'product_uos': (line.product_uos and line.product_uos.id)\
                                or line.product_uom.id,
                        'location_id': order.shop_id.warehouse_id.lot_stock_id.id,
                        'procure_method': line.type,
                        'move_id': move_id,
                        'property_ids': [(6, 0, [x.id for x in line.property_ids])],
                        'company_id': order.company_id.id,
                        'size_x':line.size_x,
                        'size_y':line.size_y,
                        'size_z':line.size_z,
                        'shape':line.shape,
                        'diameter':line.diameter,
                        'weight':line.weight,
                        'density':line.density,
                        'price_type':line.sale_price,
                    })
                    proc_ids.append(proc_id)
                    self.pool.get('sale.order.line').write(cr, uid, [line.id], {'procurement_id': proc_id})
                    if order.state == 'shipping_except':
                        for pick in order.picking_ids:
                            for move in pick.move_lines:
                                if move.state == 'cancel':
                                    mov_ids = move_obj.search(cr, uid, [('state', '=', 'cancel'),('sale_line_id', '=', line.id),('picking_id', '=', pick.id)])
                                    if mov_ids:
                                        for mov in move_obj.browse(cr, uid, mov_ids):
                                            move_obj.write(cr, uid, [move_id], {'product_qty': mov.product_qty, 'product_uos_qty': mov.product_uos_qty})
                                            proc_obj.write(cr, uid, [proc_id], {'product_qty': mov.product_qty, 'product_uos_qty': mov.product_uos_qty})

            val = {}

            if picking_id:
                wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)

            for proc_id in proc_ids:
                wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)

            if order.state == 'shipping_except':
                val['state'] = 'progress'
                val['shipped'] = False

                if (order.order_policy == 'manual'):
                    for line in order.order_line:
                        if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                            val['state'] = 'manual'
                            break
            self.write(cr, uid, [order.id], val)                                     
        return picking_id

sale_order()

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
        'weight': fields.float('Weight',),
        'purchase_price': fields.selection((('weight', 'Weight'), ('units', 'Units')), 'Price in'),
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
            result['value']['sale_price'] = product_obj.list_price
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
        'weight': fields.float('Weight',),
        'sale_price': fields.selection((('weight', 'Weight'), ('units', 'Units')), 'Price in', required=True),
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