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


from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from osv import fields, osv
from tools.translate import _
import netsvc
import tools
import decimal_precision as dp
import logging



class stock_inventory(osv.osv):
    
    _inherit='stock.inventory'
    
    
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirm the inventory and writes its finished date
        @return: True
        """
        if context is None:
            context = {}
        # to perform the correct inventory corrections we need analyze stock location by
        # location, never recursively, so we use a special context
        product_context = dict(context, compute_child=False)

        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        for inv in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for line in inv.inventory_line_id:
                pid = line.product_id.id
                product_context.update(uom=line.product_uom.id, prodlot_id=line.prod_lot_id.id, location=line.location_id.id, from_date=False, to_date=inv.date, states=['done'], what=['in', 'out'])
                amount = product_obj.get_product_available(cr, uid, [pid], product_context)[pid]
        
                change = line.product_qty - amount
                lot_id = line.prod_lot_id.id
                if change:
                    location_id = line.product_id.product_tmpl_id.property_stock_inventory.id
                    value = {
                        'name': 'INV:' + str(line.inventory_id.id) + ':' + line.inventory_id.name,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom.id,
                        'prodlot_id': lot_id,
                        'date': inv.date,
                    }
                    if change > 0:
                        value.update( {
                            'product_qty': change,
                            'location_id': location_id,
                            'location_dest_id': line.location_id.id,
                        })
                    else:
                        value.update( {
                            'product_qty': -change,
                            'location_id': line.location_id.id,
                            'location_dest_id': location_id,
                        })
                    move_ids.append(self._inventory_line_hook(cr, uid, line, value))
            message = _('Inventory') + " '" + inv.name + "' "+ _("is done.")
            self.log(cr, uid, inv.id, message)
            self.write(cr, uid, [inv.id], {'state': 'confirm', 'move_ids': [(6, 0, move_ids)]})
        return True

    
stock_inventory()



class stock_inventory_line(osv.osv):
    
    _inherit='stock.inventory.line'
    _columns = {
        'state': fields.related('inventory_id','state',type='selection', selection=[('draft', 'Draft'), ('done', 'Done'), ('confirm','Confirmed'),('cancel','Cancelled')],string='State', readonly=True),
    }

    
    def on_change_product_id(self, cr, uid, ids, location_id, product, uom=False, to_date=False, prod_lot_id=False):
        """ Changes UoM and name if product_id changes.
        @param location_id: Location id
        @param product: Changed product_id
        @param uom: UoM product
        @return:  Dictionary of changed values
        """
        if not product:
            return {'value': {'product_qty': 0.0, 'product_uom': False}}
        
        prod_context={'uom': uom, 'to_date': to_date, 'from_date':False, 'states':['done'], 'what':['in', 'out']}
        if prod_lot_id:
            prod_context.update({'prodlot_id':prod_lot_id})   
        obj_product = self.pool.get('product.product').browse(cr, uid, product)
        uom = uom or obj_product.uom_id.id
        amount = self.pool.get('stock.location')._product_get(cr, uid, location_id, [product],prod_context)[product]
        result = {'product_qty': amount, 'product_uom': uom}
        return {'value': result}
    
stock_inventory_line()