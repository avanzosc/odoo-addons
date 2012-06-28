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


class config_sale_line_final_line(osv.osv_memory):
    _name="config.sale.line.final.line"
    _columns = {
                'config_id':fields.many2one('config.sale.line', 'Config'),               
                'product_id':fields.many2one('product.product', 'Product', required=True),
                'product_uom':fields.many2one('product.uom', 'Product UoM', required=True),
                'product_qty':fields.float('Quantity', required=True, digits=(16,2)),
                'shape': fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape', required=True),
                'size_x': fields.float('Width'),
                'size_y': fields.float('Lenght'),
                'size_z': fields.float('Thickness'),
                'diameter': fields.float('Diameter'),
                'weight': fields.float('Dimension'),
                'density': fields.float('Density'),
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
    
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter, context=None):
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
config_sale_line_final_line()

class config_sale_line_line(osv.osv_memory):
    _name="config.sale.line.line"
    _columns = {
                'config_id':fields.many2one('config.sale.line', 'Config'),          
                'product_id':fields.many2one('product.product', 'Product', required=True),
                'product_uom':fields.many2one('product.uom', 'Product UoM', required=True),
                'product_qty':fields.float('Quantity', required=True, digits=(16,2)),
                'prodlot_id':fields.many2one('stock.production.lot', 'Lot'),
                'shape': fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape', required=True),
                'size_x': fields.float('Width'),
                'size_y': fields.float('Lenght'),
                'size_z': fields.float('Thickness'),
                'diameter': fields.float('Diameter'),
                'weight': fields.float('Dimension'),
                'density':fields.float('Density'),
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
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter, context=None):
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
config_sale_line_line()

class config_sale_line(osv.osv_memory):
    _name="config.sale.line"
    _columns = {
                'product_id':fields.many2one('product.product', 'Product', required=True),
                'product_uom':fields.many2one('product.uom', 'Product UoM', required=True),
                'product_qty':fields.float('Quantity', required=True, digits=(16,2)),
                'shape': fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape', required=True),
                'size_x': fields.float('Width'),
                'size_y': fields.float('Lenght'),
                'size_z': fields.float('Thickness'),
                'diameter': fields.float('Diameter'),
                'weight': fields.float('Dimension'),
                'density': fields.float('Density'),
                'line_ids': fields.one2many('config.sale.line.line', 'config_id', 'Lines'), 
                'final_line_ids':fields.one2many('config.sale.line.final.line', 'config_id', 'Final Lines'),              
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
#                'size_x':w.size_x,
#                'size_y':w.size_y,
#                'size_z':w.size_z,
#                'density':w.density,
                'shape':w.shape,
#                'diameter':w.diameter,
#                'weight':compute_w(cr, uid, factor1, factor2, factor3, factor4, w.size_x, w.size_y, w.size_z, w.shape, w.density, w.diameter)['weight']                                                                               
            }
            return {'value': v}
        return {}
    
    def compute_weight(self, cr, uid, id, product_id, size_x, size_y, size_z, shape, density, diameter, context=None):
       if product_id:
           product = self.pool.get('product.product').browse(cr, uid, product_id, context='')
           factor1 = product.uom_d_weight.factor
           factor2 = product.uom_id.factor
           factor3 = product.uom_d_size.factor
           factor4 = product.uom_s_size.factor           
           return {'value': compute_w(cr, uid, factor1, factor2, factor3, factor4, size_x, size_y, size_z, shape, density, diameter)}
   
    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param fields: List of fields for default value
        @param context: A standard dictionary for contextual values

        @return : default values of fields.
        """
        record_ids=False
        if context.get('active_model')=='sale.order' and context.get('is_first')==True:
            active_ids = context.get('active_ids')
            product_obj = self.pool.get('product.product')
            sale_line_obj = self.pool.get('sale.order.line')
    
            product_list = product_obj.search(cr,uid,[('type','in',('product', 'consu')), ('supply_method','=','produce')])
            line_ids = sale_line_obj.search(cr,uid,[('order_id','in', active_ids), ('product_id', 'in', product_list),('shape', 'in', ('quadrangular', 'cylindrical')),('type', '=','make_to_order' )])
            context.update({'is_first':False, 'active_ids':line_ids})
        
        record_ids = context and context.get('active_ids', False) or False
        res = super(config_sale_line, self).default_get(cr, uid, fields, context=context)
        if not record_ids:
            return {'type': 'ir.actions.act_window_close'}
        else:
            record_id = record_ids[0]
 
            sale_line = self.pool.get('sale.order.line').browse(cr, uid, record_id, context=context)
            if 'product_id' in fields:
                product_id = False
                if sale_line.maker_id:
                    product_id = sale_line.maker_id.product_id.id
                elif sale_line.product_id:
                    product_id = sale_line.product_id.id 
                res.update({'product_id': product_id})
            if 'product_uom' in fields:
                product_uom = False
                if sale_line.maker_id:
                    product_uom = sale_line.maker_id.product_uom.id
                if not product_uom: 
                    if sale_line.product_uom:
                        product_uom = sale_line.product_uom.id 
                    else:
                        product_uom = sale_line.product_id.uom_id.id 
                res.update({'product_uom': product_uom})
            if 'product_qty' in fields:
                product_qty = 0.0
                if sale_line.maker_id:
                    product_qty = sale_line.maker_id.product_qty
                elif sale_line.product_uom_qty:
                    product_qty = sale_line.product_uom_qty
                res.update({'product_qty': product_qty})
            if 'shape' in fields:
                shape = 'other'
                if sale_line.maker_id:
                    shape = sale_line.maker_id.shape
                elif sale_line.shape:
                    shape = sale_line.shape
                if shape == 'cylindrical':
                    res.update({'shape':'cylindrical'})
                elif shape == 'quadrangular':
                    res.update({'shape':'quadrangular'})
                else:
                    res.update({'shape':'other'})
            if 'size_x' in fields:
                size_x = 0.0
                if sale_line.maker_id:
                    size_x = sale_line.maker_id.size_x
                elif sale_line.size_x:
                    size_x = sale_line.size_x
                res.update({'size_x': size_x})
            if 'size_y' in fields:
                size_y = 0.0
                if sale_line.maker_id:
                    size_y = sale_line.maker_id.size_y
                elif sale_line.size_y:
                    size_y = sale_line.size_y
                res.update({'size_y': size_y})
            if 'size_z' in fields:
                size_z = 0.0
                if sale_line.maker_id:
                    size_z = sale_line.maker_id.size_z
                elif sale_line.size_z:
                    size_z = sale_line.size_z
                res.update({'size_z': size_z})
            if 'diameter' in fields:
                diameter = 0.0
                if sale_line.maker_id:
                    diameter = sale_line.maker_id.diameter
                else:
                    diameter = sale_line.diameter
                res.update({'diameter': diameter})
            if 'weight' in fields:
                weight = 0.0
                if sale_line.maker_id:
                    weight = sale_line.maker_id.weight
                elif sale_line.weight:
                    weight = sale_line.weight
                res.update({'weight': weight})
            if 'density' in fields:
                density = 0.0
                if sale_line.maker_id:
                    density = sale_line.maker_id.density
                elif sale_line.density:
                    density = sale_line.density
                res.update({'density': density})
            if 'line_ids' in fields:
                id_list = []
                sale_line_line_obj = self.pool.get('config.sale.line.line')
                if sale_line.maker_id:
                    for line in sale_line.maker_id.line_ids:
                        val = {
                               'product_id':line.product_id.id,
                               'product_qty':line.product_qty,
                               'product_uom':line.product_uom.id,
                               'size_x': line.size_x,
                               'size_y':line.size_y,
                               'size_z':line.size_z,
                               'diameter':line.diameter,
                               'weight': line.weight,
                               'shape':line.shape,    
                               'density':line.density,
                               }
                        id_list.append(val)
                else:
                    bom_obj = self.pool.get('mrp.bom')
                    bom_id = bom_obj.search(cr,uid,[('product_id', '=', sale_line.product_id.id)])
                    if bom_id:
                        bom_o = bom_obj.browse(cr,uid,bom_id[0])
                        if bom_o:
                            for line in bom_o.bom_lines:
                                val = {
                                       'product_id':line.product_id.id,
                                       'product_qty':line.product_qty,
                                       'product_uom':line.product_uom.id,
                                       'shape':line.product_id.shape,
                                       'size_x': 0.0,
                                       'size_y':0.0,
                                       'size_z':0.0,
                                       'diameter':0.0,
                                       'weight': 0.0,
                                       'density':0.0,
                                       }
                                id_list.append(val)
                res.update({'line_ids': id_list})
            if 'final_line_ids' in fields:
                fid_list = []
                sale_line_line_obj = self.pool.get('config.sale.line.final.line')
                if sale_line.maker_id:
                    for line in sale_line.maker_id.final_line_ids:
                        val = {
                               'product_id':line.product_id.id,
                               'product_qty':line.product_qty,
                               'product_uom':line.product_uom.id,
                               'size_x': line.size_x,
                               'size_y':line.size_y,
                               'size_z':line.size_z,
                               'diameter':line.diameter,
                               'weight': line.weight,
                               'shape':line.shape,    
                               'density':line.density,
                               }
                        fid_list.append(val)
                res.update({'final_line_ids': fid_list})
        return res

    def button_ok(self, cr, uid, ids, context=None):
        res={}
        maker_obj = self.pool.get('mrp.maker')
        maker_line_obj = self.pool.get('mrp.maker.line')
        maker_final_line_obj = self.pool.get('mrp.maker.final.line')
        sale_line_obj = self.pool.get('sale.order.line')  
        pl_obj = self.pool.get('mrp.production.product.line')
        pc_obj = self.pool.get('stock.move')
        lot_obj = self.pool.get('stock.production.lot')
        
        if context.get('active_model')=='sale.order' and context.get('is_first')==True:
            active_ids = context.get('active_ids')
            product_obj = self.pool.get('product.product')
            sale_line_obj = self.pool.get('sale.order.line')
    
            product_list = product_obj.search(cr,uid,[('type','in',('product', 'consu')), ('supply_method','=','produce')])
            line_ids = sale_line_obj.search(cr,uid,[('order_id','in', active_ids), ('product_id', 'in', product_list), ('type', '=','make_to_order' ), ('shape', 'in', ('quadrangular', 'cylindrical'))])
            context.update({'is_first':False, 'active_ids':line_ids})   
        record_ids = context and context.get('active_ids', False) or False
        if record_ids:
            record_id = record_ids[0]
            for wiz in self.browse(cr,uid,ids):
                sale_line = sale_line_obj.browse(cr, uid, record_id, context=context)
                
                val = {
                       'product_id':wiz.product_id.id,
                       'product_qty':wiz.product_qty,
                       'product_uom':wiz.product_uom.id,
                       'shape':wiz.shape,
                       'size_x':wiz.size_x,
                       'size_y':wiz.size_y,
                       'size_z':wiz.size_z,
                       'diameter':wiz.diameter,
                       'weight':wiz.weight,
                       'density':wiz.density,
                       }
                maker_id = False
                if sale_line.maker_id:
                    maker_id = sale_line.maker_id.id
                    maker_obj.write(cr,uid,[maker_id],val)
                    for ml in sale_line.maker_id.line_ids:
                        maker_line_obj.unlink(cr,uid,[ml.id])
                    for mp in sale_line.maker_id.final_line_ids:
                        maker_final_line_obj.unlink(cr,uid,[mp.id])
                else:
                    maker_id = maker_obj.create(cr,uid,val)
                val.update({'maker_id':maker_id})
                sale_line_obj.write(cr,uid,[record_id],val)
                for line in wiz.line_ids:
                    val_l = {
                       'product_id':line.product_id.id,
                       'product_qty':line.product_qty,
                       'product_uom':line.product_uom.id,
                       'shape':line.shape,
                       'size_x':line.size_x,
                       'size_y':line.size_y,
                       'size_z':line.size_z,
                       'diameter':line.diameter,
                       'weight':line.weight,
                       'maker_id':maker_id,
                       'density':line.density,
                       }
                    maker_line_obj.create(cr,uid,val_l)
                res_list=[]
                for f_line in wiz.final_line_ids:
                    val_fl = {
                       'product_id':f_line.product_id.id,
                       'product_qty':f_line.product_qty,
                       'product_uom':f_line.product_uom.id,
                       'shape':f_line.shape,
                       'size_x':f_line.size_x,
                       'size_y':f_line.size_y,
                       'size_z':f_line.size_z,
                       'diameter':f_line.diameter,
                       'weight':f_line.weight,
                       'maker_id':maker_id,
                       'density':f_line.density,
                       }
                    maker_final_line_obj.create(cr,uid,val_fl)
                    
            active_list = context.get('active_ids')
            active_list.pop(0)
            context.update({'active_ids':active_list})
            if active_list:
                res={   'type': 'ir.actions.act_window',
                        'res_model': 'config.sale.line',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'target': 'new',
                        'context':context
                    }
            else:
                res = {'type': 'ir.actions.act_window_close'}
        else:
            res = {'type': 'ir.actions.act_window_close'}
        
        return res
config_sale_line()