
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

class mrp_production_product_line(osv.osv): 

    _inherit = 'mrp.production.product.line'
    
    _columns = {'supply_method': fields.selection([('produce','Produce'),('buy','Buy'),('buy/produce','Buy/Produce')], 'Supply method', required=True, help="Produce will generate production order or tasks, according to the product type. Purchase will trigger purchase orders when requested."),
                'buy_produce':fields.boolean('Buy/Produce'), 
                }
    
    def create(self, cr, uid, data, context=None):
        if context == None:
            context = {}
            
        new_id = super(mrp_production_product_line,self).create(cr,uid,data,context)
        
        line = self.browse(cr,uid,new_id,context=context)
        
        if line.product_id.supply_method == 'buy/produce':
            buy_produce = True
        else:
            buy_produce = False
        
        self.write(cr,uid,[new_id],{'supply_method': line.product_id.supply_method,
                                    'buy_produce': buy_produce,})
        
        return new_id 
    
mrp_production_product_line()