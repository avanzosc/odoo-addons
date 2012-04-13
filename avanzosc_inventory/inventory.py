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
class product_uom(osv.osv):
    _inherit='product.uom'
    def _compute_qty_obj(self, cr, uid, from_unit, qty, to_unit, context=None):
        if context is None:
            context = {}
        if from_unit.category_id.id <> to_unit.category_id.id:
            if context.get('raise-exception', True):
                raise osv.except_osv(_('Error !'), _('Conversion from Product UoM %s to Default UoM %s is not possible as they both belong to different Category!.') % (from_unit.name,to_unit.name,))
            else:
                return qty
        amount = qty / from_unit.factor
        return amount
product_uom()
class product_product(osv.osv):
    
    
    _inherit='product.product'
    
    
    def get_product_available_lot(self, cr, uid, ids, context=None):
        """ Finds whether product is available or not in particular warehouse.
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        states = context.get('states',[])
        what = context.get('what',())
        if not ids:
            ids = self.search(cr, uid, [])
        res = {}.fromkeys(ids, 0.0)
        if not ids:
            return res

    # TODO: write in more ORM way, less queries, more pg84 magic
        if context.get('shop', False):
            cr.execute('select warehouse_id from sale_shop where id=%s', (int(context['shop']),))
            res2 = cr.fetchone()
            if res2:
                context['warehouse'] = res2[0]

        if context.get('warehouse', False):
            cr.execute('select lot_stock_id from stock_warehouse where id=%s', (int(context['warehouse']),))
            res2 = cr.fetchone()
            if res2:
                context['location'] = res2[0]

        if context.get('location', False):
            if type(context['location']) == type(1):
                location_ids = [context['location']]
            elif type(context['location']) in (type(''), type(u'')):
                location_ids = self.pool.get('stock.location').search(cr, uid, [('name','ilike',context['location'])], context=context)
            else:
                location_ids = context['location']
        else:
            location_ids = []
            wids = self.pool.get('stock.warehouse').search(cr, uid, [], context=context)
            for w in self.pool.get('stock.warehouse').browse(cr, uid, wids, context=context):
                location_ids.append(w.lot_stock_id.id)

        # build the list of ids of children of the location given by id
        if context.get('compute_child',True):
            child_location_ids = self.pool.get('stock.location').search(cr, uid, [('location_id', 'child_of', location_ids)])
            location_ids = child_location_ids or location_ids
        else:
            location_ids = location_ids

        uoms_o = {}
        product2uom = {}
        for product in self.browse(cr, uid, ids, context=context):
            product2uom[product.id] = product.uom_id.id
            uoms_o[product.uom_id.id] = product.uom_id

        results = []
        results2 = []
        prodlot_id = context.get('prodlot_id', False)
        if prodlot_id:
            prodlot_id = ('IN (' + str(prodlot_id) + ')')
        else:
            prodlot_id = 'is null'
        
        
        from_date = context.get('from_date',False)
        to_date = context.get('to_date',False)
        date_str = False
        date_values = False
        where = [tuple(location_ids),tuple(location_ids),tuple(ids),tuple(states)]
        if from_date and to_date:
            date_str = "date>=%s and date<=%s"
            where.append(tuple([from_date]))
            where.append(tuple([to_date]))
        elif from_date:
            date_str = "date>=%s"
            date_values = [from_date]
        elif to_date:
            date_str = "date<=%s"
            date_values = [to_date]

        query =  ('select sum(product_qty), product_id, product_uom '\
                'from stock_move '\
                'where location_id NOT IN %s '\
                'and location_dest_id IN %s '\
                'and product_id IN %s '\
                'and prodlot_id ' + prodlot_id +' '\
                'and state IN %s ' + (date_str and 'and '+date_str+' ' or '') +' '\
                'group by product_id,product_uom',tuple(where))
    # TODO: perhaps merge in one query.
        if date_values:
            where.append(tuple(date_values))
        if 'in' in what:
            # all moves from a location out of the set to a location in the set
            cr.execute(
                'select sum(product_qty), product_id, product_uom '\
                'from stock_move '\
                'where location_id NOT IN %s '\
                'and location_dest_id IN %s '\
                'and product_id IN %s '\
                'and prodlot_id ' + prodlot_id +' '\
                'and state IN %s ' + (date_str and 'and '+date_str+' ' or '') +' '\
                'group by product_id,product_uom',tuple(where))
            results = cr.fetchall()
        if 'out' in what:
            # all moves from a location in the set to a location out of the set
            cr.execute(
                'select sum(product_qty), product_id, product_uom '\
                'from stock_move '\
                'where location_id IN %s '\
                'and location_dest_id NOT IN %s '\
                'and product_id  IN %s '\
                'and prodlot_id ' + prodlot_id +' '\
                'and state in %s ' + (date_str and 'and '+date_str+' ' or '') + ' '\
                'group by product_id,product_uom',tuple(where))
            results2 = cr.fetchall()
        uom_obj = self.pool.get('product.uom')
        uoms = map(lambda x: x[2], results) + map(lambda x: x[2], results2)
        if context.get('uom', False):
            uoms += [context['uom']]

        uoms = filter(lambda x: x not in uoms_o.keys(), uoms)
        if uoms:
            uoms = uom_obj.browse(cr, uid, list(set(uoms)), context=context)
            for o in uoms:
                uoms_o[o.id] = o
        #TOCHECK: before change uom of product, stock move line are in old uom.
        context.update({'raise-exception': False})
        for amount, prod_id, prod_uom in results:
            amount = uom_obj._compute_qty_obj(cr, uid, uoms_o[prod_uom], amount,
                     uoms_o[context.get('uom', False) or product2uom[prod_id]], context=context)
            res[prod_id] += amount
        for amount, prod_id, prod_uom in results2:
            amount = uom_obj._compute_qty_obj(cr, uid, uoms_o[prod_uom], amount,
                    uoms_o[context.get('uom', False) or product2uom[prod_id]], context=context)
            res[prod_id] -= amount
        return res
product_product()

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
#        product_context = dict(context, compute_child=False)
        product_context={}
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        for inv in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for line in inv.inventory_line_id:
                pid = line.product_id.id
                lot_id = False
                if line.prod_lot_id:
                    lot_id = line.prod_lot_id.id
                product_context.update(uom=line.product_uom.id, prodlot_id=lot_id, location=line.location_id.id, from_date=False, to_date=inv.date, states=['done'], what=['in', 'out'])
                amount = product_obj.get_product_available_lot(cr, uid, [pid], product_context)[pid]
        
                change = line.product_qty - amount

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
	product_obj = self.pool.get('product.product')        
	if not product:
            return {'value': {'product_qty': 0.0, 'product_uom': False}}
        
        prod_context={'uom': uom, 'to_date': to_date, 'from_date':False, 'states':['done'], 'what':['in', 'out']}
        if prod_lot_id:
            prod_context.update({'prodlot_id':prod_lot_id})   
        obj_product = product_obj.browse(cr, uid, product)
        uom = uom or obj_product.uom_id.id
	prod_context.update(location=location_id)
        amount = product_obj.get_product_available_lot(cr, uid, [product], prod_context)[product]
        result = {'product_qty': amount, 'product_uom': uom}
        return {'value': result}
    
stock_inventory_line()
