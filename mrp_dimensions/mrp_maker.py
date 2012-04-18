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

class mrp_maker(osv.osv):
    
    _name='mrp.maker'
    
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
                'weight': fields.float('Weight'),
                'line_ids':fields.one2many('mrp.maker.line','maker_id', 'Lines'),
                'sale_line':fields.many2one('sale.order.line', 'Sale line'),
                }    
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
                'weight': fields.float('Weight'),
                'maker_id':fields.many2one('mrp.maker', 'Parent'),
                }    
    
mrp_maker_line()

