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


class config_mrp_final_line(osv.osv_memory):
    _name="config.mrp.final.line"
    _columns = {
                'config_id':fields.many2one('config.mrp', 'Config'),               
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
config_mrp_final_line()

class config_mrp_line(osv.osv_memory):
    _name="config.mrp.line"
    _columns = {
                'config_id':fields.many2one('config.mrp', 'Config'),          
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
config_mrp_line()

class config_mrp(osv.osv_memory):
    _name="config.mrp"
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
                'line_ids': fields.one2many('config.mrp.line', 'config_id', 'Lines'), 
                'final_line_ids':fields.one2many('config.mrp.final.line', 'config_id', 'Final Lines'),              
                }  
    
    def view_init(self, cr, uid, fields, context=None):
        if context is None:
            context={}

        mrp_ids =  context.get('active_ids',[])
        if mrp_ids:
            mrp = self.pool.get('mrp.production').browse(cr,uid,mrp_ids)
            for mrp_o in mrp:
                if (mrp_o.state != 'draft' ):
                    raise osv.except_osv(_('Error!'), _("You can't reconfigure, %s order.")%(mrp_o.state,))
                else:
                    if not mrp_o.bom_id:
                        raise osv.except_osv(_('Error!'), _("You have to asign BOM to the order."))
        return False
    
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
        record_id = context and context.get('active_id', False) or False
        res = super(config_mrp, self).default_get(cr, uid, fields, context=context)

        if record_id:
            mrp = self.pool.get('mrp.production').browse(cr, uid, record_id, context=context)
            if 'product_id' in fields:
                product_id = False
                if mrp.maker:
                    product_id = mrp.maker.product_id.id
                elif mrp.product_id:
                    product_id = mrp.product_id.id 
                res.update({'product_id': product_id})
            if 'product_uom' in fields:
                product_uom = False
                if mrp.maker:
                    product_uom = mrp.maker.product_uom.id
                if not product_uom: 
                    if mrp.product_uom:
                        product_uom = mrp.product_uom.id 
                    else:
                        product_uom = mrp.product_id.uom_id.id 
                res.update({'product_uom': product_uom})
            if 'product_qty' in fields:
                product_qty = 0.0
                if mrp.maker:
                    product_qty = mrp.maker.product_qty
                elif mrp.product_qty:
                    product_qty = mrp.product_qty
                res.update({'product_qty': product_qty})
            if 'shape' in fields:
                shape = 'other'
                if mrp.maker:
                    shape = mrp.maker.shape
                elif mrp.shape:
                    shape = mrp.shape
                if shape == 'cylindrical':
                    res.update({'shape':'cylindrical'})
                elif shape == 'quadrangular':
                    res.update({'shape':'quadrangular'})
                else:
                    res.update({'shape':'other'})
            if 'size_x' in fields:
                size_x = 0.0
                if mrp.maker:
                    size_x = mrp.maker.size_x
                elif mrp.size_x:
                    size_x = mrp.size_x
                res.update({'size_x': size_x})
            if 'size_y' in fields:
                size_y = 0.0
                if mrp.maker:
                    size_y = mrp.maker.size_y
                elif mrp.size_y:
                    size_y = mrp.size_y
                res.update({'size_y': size_y})
            if 'size_z' in fields:
                size_z = 0.0
                if mrp.maker:
                    size_z = mrp.maker.size_z
                elif mrp.size_z:
                    size_z = mrp.size_z
                res.update({'size_z': size_z})
            if 'diameter' in fields:
                diameter = 0.0
                if mrp.maker:
                    diameter = mrp.maker.diameter
                elif mrp.diameter:
                    diameter = mrp.diameter
                res.update({'diameter': diameter})
            if 'weight' in fields:
                weight = 0.0
                if mrp.maker:
                    weight = mrp.maker.weight
                elif mrp.weight:
                    weight = mrp.weight
                res.update({'weight': weight})
            if 'density' in fields:
                density = 0.0
                if mrp.maker:
                    density = mrp.maker.density
                elif mrp.density:
                    density = mrp.density
                res.update({'density': density})
            if 'line_ids' in fields:
                id_list = []
                mrp_line_obj = self.pool.get('config.mrp.line')
                if mrp.maker:
                    for line in mrp.maker.line_ids:
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
                elif mrp.product_lines:
                    for line in mrp.product_lines:
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
                    bom_id = mrp.bom_id.id
                    if not bom_id:
                        bom_id = bom_obj.search(cr,uid,[('product_id', '=', mrp.product_id.id)])[0]
                    if bom_id:
                        bom_o = bom_obj.browse(cr,uid,bom_id)
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
                mrp_line_obj = self.pool.get('config.mrp.final.line')
                if mrp.maker:
                    for line in mrp.maker.final_line_ids:
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
        mrp_obj = self.pool.get('mrp.production')  
        pl_obj = self.pool.get('mrp.production.product.line')
        pc_obj = self.pool.get('stock.move')
        lot_obj = self.pool.get('stock.production.lot')
        
            
        record_id = context and context.get('active_id', False) or False
        if record_id:
            for wiz in self.browse(cr,uid,ids):
                mrp = mrp_obj.browse(cr, uid, record_id, context=context)
                for pl in mrp.product_lines:
                    pl_obj.unlink(cr,uid,[pl.id])
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
                if mrp.maker:
                    maker_id = mrp.maker.id
                    maker_obj.write(cr,uid,[maker_id],val)
                    for ml in mrp.maker.line_ids:
                        maker_line_obj.unlink(cr,uid,[ml.id])
                    for mp in mrp.maker.final_line_ids:
                        maker_final_line_obj.unlink(cr,uid,[mp.id])
                else:
                    maker_id = maker_obj.create(cr,uid,val)
                val.update({'maker':maker_id})
                mrp_obj.write(cr,uid,[record_id],val)
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
                    val_l.update({'production_id':record_id, 'name':line.product_id.name})
                    pl_obj.create(cr,uid,val_l)
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
                    val_lot = {
                       'product_id':f_line.product_id.id,
                       'shape':f_line.shape,
                       'size_x':f_line.size_x,
                       'size_y':f_line.size_y,
                       'size_z':f_line.size_z,
                       'diameter':f_line.diameter,
                       'weight':f_line.weight,
                       'density':f_line.density,
                       }
                    maker_final_line_obj.create(cr,uid,val_fl)
                    
                    source = mrp.product_id.product_tmpl_id.property_stock_production.id
                    dest = mrp.location_dest_id.id
                    lot_o = False
                    lot_domain = [('product_id', '=', f_line.product_id.id),('shape', '=', f_line.shape),('size_x', '=', f_line.size_x),('size_y', '=', f_line.size_y),('size_z','=', f_line.size_z),('diameter', '=', f_line.diameter),('weight', '=', f_line.weight),('density', '=', f_line.density)]
                    lot = lot_obj.search(cr,uid,lot_domain)
                    if lot:
                       lot_o=lot[0]
                    else:
                        lot_o = lot_obj.create(cr,uid,val_lot)
                        lot_obj.generate_serial(cr,uid,[lot_o]) 
                    val_fl.update({'name':f_line.product_id.name, 'location_id':source, 'location_dest_id':dest, 'prodlot_id':lot_o})
                    pc_id = pc_obj.create(cr,uid,val_fl)
                    res_list.append(pc_id)
                mrp_obj.write(cr, uid, [record_id], {'move_created_ids': [(6, 0, res_list)]}) 
        return res
config_mrp()