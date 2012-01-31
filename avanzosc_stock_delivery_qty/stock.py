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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

from osv import osv, fields
from tools.translate import _

import decimal_precision as dp
import netsvc


class stock_inventory_line(osv.osv):
    _inherit = 'stock.inventory.line'
    _columns = {
        'inventory_id': fields.many2one('stock.inventory', 'Inventory', ondelete='cascade', select=True, states={'draft':[('readonly',False)]}),
        'location_id': fields.many2one('stock.location', 'Location', required=True, states={'draft':[('readonly',False)]}),
        'product_id': fields.many2one('product.product', 'Product', required=True, select=True, states={'draft':[('readonly',False)]}),
        'product_uom': fields.many2one('product.uom', 'Product UOM', required=True, states={'draft':[('readonly',False)]}),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product UoM'),states={'done':[('readonly',True)]}),
        'prod_lot_id': fields.many2one('stock.production.lot', 'Production Lot', domain="[('product_id','=',product_id)]", states={'draft':[('readonly',False)]}),
        'state': fields.related('inventory_id','state',type='selection', selection=[('draft', 'Draft'), ('done', 'Done'), ('confirm','Confirmed'),('cancel','Cancelled')],string='State',store=True, readonly=True),
    }
stock_inventory_line()