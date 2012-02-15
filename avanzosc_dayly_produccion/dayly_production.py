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

class dayly_production(osv.osv):
    
    _name = "dayly.production"
    
    _columns = {
              'date':fields.date('Date', readonly=True),
              'day':fields.char('Day', size=34, readonly=True),
              'granja':fields.many2one('stock.location', 'Granja', readonly=True),
              'nave':fields.many2one('stock.location', 'Nave', readonly=True),
              'prodlot_id':fields.many2one('stock.production.lot', 'Lot', readonly=True),
              'week_age':fields.float('Age', readonly=True),
              'bajas_gall':fields.integer('Bajas gallinas', readonly=True),
              'existencias_gall':fields.integer('Gallinas presentes', readonly=True),
              'egg_sc_prod_qty':fields.integer('SC Egg production qty', readonly=True),
              'egg_sc_prod_kg':fields.float('SC Egg production kg.', readonly=True),
              'egg_sc_sale_qty':fields.integer('SC Egg sale qty', readonly=True),
              'egg_sc_sale_kg':fields.float('SC Egg sale kg', readonly=True),
              'egg_su_prod_qty':fields.integer('SU Egg production qty', readonly=True),
              'egg_su_prod_kg':fields.float('SU Egg production kg.', readonly=True),
              'egg_su_sale_qty':fields.integer('SU Egg sale qty', readonly=True),
              'egg_su_sale_kg':fields.float('SU Egg sale kg', readonly=True),
              'egg_prod_qty':fields.integer('Egg production qty', readonly=True),
              'egg_prod_kg':fields.float('Egg production kg.', readonly=True),
              'egg_sale_qty':fields.integer('Egg sale qty', readonly=True),
              'egg_sale_kg':fields.float('Egg sale kg', readonly=True),
              'egg_weight':fields.float('Egg weight', readonly=True),
              'all_egg_qty':fields.float('All egg qty.', readonly=True),
              'feed_entries':fields.float('Feed entries', readonly=True),
              'feed_diff':fields.float('Feed diff', readonly=True),
              'feed_inv':fields.float('Feed inv.', readonly=True),
              'water_consum':fields.float('Water consum', readonly=True),
              'max_temp':fields.float('Max. temp.', readonly=True),
              'min_temp':fields.float('Min. temp.', readonly=True),
              }
    
    ## CALCULO DE LA CANTIDAD DE GALLINAS QUE SE HAN SACADO DE LA NAVE A UNA FECHA
    def _get_gall_baj(self, cr, uid, ids, date, lot, context=None):
        qty = 0.0
        end_date = datetime.strptime(date, "%Y-%m-%d") + relativedelta(days= +1) 
        end_date = datetime.strftime(end_date, "%Y-%m-%d")
        loc_obj = self.pool.get('stock.location')
        move_obj = self.pool.get('stock.move')
        prod_id = loc_obj.search(cr, uid, [('name', 'like', 'Bajas Gallinas')])
        if prod_id:
            loc = prod_id[0]
            move_list = move_obj.search(cr, uid, [('prodlot_id', '=', lot), ('location_dest_id', '=', loc), ('date', '<=', date), ('date', '>=', date), ('state', '=', 'done')])
            for move in move_list:
                move_o = move_obj.browse(cr, uid, move)
                qty += move_o.product_qty
        return qty
    
    ## CALCULAR LA EDAD DE LAS GALLINAS A UNA FECHA DETERMINADA
    def _get_week_age(self, cr, uid, ids, date, lot, context=None):
        age = 0
        prod_obj = self.pool.get('estirpe.lot.prevision')
        prod_list = prod_obj.search(cr, uid, [('lot', '=', lot)])
        if prod_list:
            born_date = prod_obj.browse(cr, uid, prod_list[0]).nac_date 
            age = datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(born_date, "%Y-%m-%d")
            age = float(age.days) / 7
        return age
    
    ## SACAR LAS UBICACIONES NAVE Y GRANJA DE UN LOTE  
    def _get_locations(self, cr, uid, ids, lot, context=None):
        location_list = []
        
        prod_obj = self.pool.get('estirpe.lot.prevision')
        loc_obj = self.pool.get('stock.location')
        prod_list = prod_obj.search(cr, uid, [('lot', '=', lot)])
        if prod_list:
            nave = prod_obj.browse(cr, uid, prod_list[0]).location2
            granja = nave.location_id.location_id 
            location_list.append(nave.id)
            location_list.append(granja.id)
        return location_list
    def _get_gall_pre(self, cr, uid, ids, date, lot, context=None):
        qty = 0
        move_obj = self.pool.get('stock.move')
        prod_obj = self.pool.get('estirpe.lot.prevision')
        prod_list = prod_obj.search(cr, uid, [('lot', '=', lot)])
        if prod_list:
            nave = prod_obj.browse(cr, uid, prod_list[0]).location2.id
            entries = move_obj.search(cr, uid, [('prodlot_id', '=', lot), ('date', '<=', date), ('location_dest_id', '=', nave), ('state', '=', 'done')])
            salidas = move_obj.search(cr, uid, [('prodlot_id', '=', lot), ('date', '<=', date), ('location_id', '=', nave), ('state', '=', 'done')])
            for entrie in entries:
                qty = qty + move_obj.browse(cr, uid, entrie).product_qty
            for salida in salidas:
                qty = qty - move_obj.browse(cr, uid, salida).product_qty
        return qty
    def _get_dayly_info(self, cr, uid, ids, date, lot, context=None):
        
        dayly_obj = self.pool.get('dayly.part')
        
        PMH = 0.0
        water_consum = 0.0
        temp_max = 0.0
        temp_min = 0.0
        
        dayly_ids = dayly_obj.search(cr, uid, [('prodlot_id', '=', lot), ('date', '=', date)])
        if dayly_ids:
            dayly_o = dayly_obj.browse(cr, uid, dayly_ids[0])
            PMH = dayly_o.eggs_weigth
            water_consum = dayly_o.water_consum
            temp_max = dayly_o.max_temp
            temp_min = dayly_o.min_temp
        
        return_list = [PMH, water_consum, temp_max, temp_min]
        return return_list
    
    def _get_feed_info(self,cr,uid,ids,date,lot,loc,context=None):
        entries = 0.0
        consum = 0.0
        invent = 0.0
        loc_id_list=[]
        cat_list = []
        
        loc_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        inv_obj = self.pool.get('stock.inventory')
        inv_line_obj = self.pool.get('stock.inventory.line')
        move_obj = self.pool.get('stock.move')
        comp_obj = self.pool.get('res.company')
        
        loc_list = loc_obj.browse(cr,uid,loc).location_id.child_ids
        for loc in loc_list:
            loc_id_list.append(loc.id)
            
        com_id = comp_obj.search(cr, uid, [])
        feed_cat = comp_obj.browse(cr, uid, com_id[0]).cat_feed_ids
        for cat in feed_cat:
            cat_list.append(cat.id)
        feed_list = product_obj.search(cr, uid, [('categ_id', 'in', cat_list)])  
        
        entrie_list = move_obj.search(cr,uid,[('location_dest_id','in',loc_id_list),('state','=','done'), ('product_id', 'in', feed_list), ('date', '<=', date), ('date', '>=', date)])
        for entrie in entrie_list:
            entries = entries + move_obj.browse(cr,uid,entrie).product_qty
        
        inventories = inv_obj.search(cr,uid,[('state','=','done'), ('date', '<=', date), ('date', '>=', date)])
        inv_list = inv_line_obj.search(cr,uid,[('location_id','in', loc_id_list),('product_id','in',feed_list),('inventory_id','in',inventories)])
        for inv_line in inv_list:
            invent = invent + inv_line_obj.browse(cr,uid,inv_line).product_qty
            
        result = [entries,consum,invent]
        return result
    
    def _get_egg_info(self,cr,uid,ids,date,lot,loc,pmh,context=None):
        product_qty = 0.0
        product_kg = 0.0
        sold_qty=0.0
        sold_kg=0.0
        cat_list = []
        
        move_obj = self.pool.get('stock.move')
        loc_obj = self.pool.get('stock.location')
        comp_obj = self.pool.get('res.company')
        product_obj = self.pool.get('product.product')
        lot_obj = self.pool.get('stock.production.lot')
        
        egg_loc = loc_obj.search(cr,uid,['|',('egg_production', '=', True),('usage','=','inventory')])
        client_loc = loc_obj.search(cr,uid,['|',('usage', '=', 'customer'),('usage','=','inventory')])
        
        com_id = comp_obj.search(cr, uid, [])
        egg_cat = comp_obj.browse(cr, uid, com_id[0]).cat_egg_ids
        for cat in egg_cat:
            cat_list.append(cat.id)
        egg_list = product_obj.search(cr, uid, [('categ_id', 'in', cat_list)])          
        
        lot_name = lot_obj.browse(cr,uid,lot).name
        lot_list = lot_obj.search(cr,uid,[('name','like',lot_name), ('product_id','in',egg_list)])
        
        
  
        produced_all_list = move_obj.search(cr,uid,[('location_dest_id','not in', client_loc ),('prodlot_id','in',lot_list),('state','=','done'), ('date', '<=', date)])
        sold_all_list = move_obj.search(cr,uid,[('location_dest_id','in', client_loc ),('prodlot_id','in',lot_list),('state','=','done'), ('date', '<=', date)])
        egg_entries =  move_obj.search(cr,uid,[('location_id','in',egg_loc),('location_dest_id','=',loc), ('product_id','in', egg_list),('state','=','done'), ('date', '<=', date)])
        egg_exit = move_obj.search(cr,uid,[('location_id','=',loc), ('product_id','in', egg_list),('state','=','done'), ('date', '<=', date)])
        
        sum_lot_qty = 0.0
        for lot_id in produced_all_list:
            sum_lot_qty = sum_lot_qty + (move_obj.browse(cr,uid,lot_id).prodlot_id.egg_qty * move_obj.browse(cr,uid,lot_id).product_qty)
        for sold_all_line in sold_all_list:
            sold_all_o = move_obj.browse(cr,uid,sold_all_line)
            sum_lot_qty = sum_lot_qty - (sold_all_o.prodlot_id.egg_qty * sold_all_o.product_qty)
            if sold_all_o.date >= date:
                sold_qty = sold_qty + (sold_all_o.prodlot_id.egg_qty * sold_all_o.product_qty)
        for egg_entrie in egg_entries:
            egg_entrie_o = move_obj.browse(cr,uid,egg_entrie)
            sum_lot_qty = sum_lot_qty + egg_entrie_o.product_qty
            if egg_entrie_o.date >= date:
                product_qty = product_qty + egg_entrie_o.product_qty
        for egg_exit_line in egg_exit:
            sum_lot_qty = sum_lot_qty - move_obj.browse(cr,uid,egg_exit_line).product_qty
    
    
        product_kg = product_qty * pmh
        sold_kg = sold_qty * pmh
        result = [product_qty, product_kg, sold_qty, sold_kg, sum_lot_qty]
        
        return result
    
    
    
    
    def calc_data(self, cr, uid, ids, start_date, end_date,context=None):
        print "START!!!!  " + time.strftime('%H:%M:%S')
        comp_obj = self.pool.get('res.company')
        product_obj = self.pool.get('product.product')
        lot_obj = self.pool.get('stock.production.lot')
        today = time.strftime('%Y-%m-%d')
        if today < end_date:
            date_end = today
        else:
            date_end = end_date
        redate = datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(days=-1) 
        date = datetime.strftime(redate, "%Y-%m-%d")
        cat_list = []
        com_id = comp_obj.search(cr, uid, [])
        gall_cat = comp_obj.browse(cr, uid, com_id[0]).cat_chicken_ids
        for cat in gall_cat:
            cat_list.append(cat.id)
        gall_prod = product_obj.search(cr, uid, [('categ_id', 'in', cat_list)])
        lot_list = lot_obj.search(cr, uid, [('product_id', 'in', gall_prod), ('stock_available', '>', 0)])
        while date != date_end:
            redate = datetime.strptime(date, "%Y-%m-%d") + relativedelta(days= +1)  
            date = datetime.strftime(redate, "%Y-%m-%d")
            for lot in lot_list:
                
                gall_baj = self._get_gall_baj(cr, uid, ids, date, lot, context)
                week_age = self._get_week_age(cr, uid, ids, date, lot, context)
                locations = self._get_locations(cr, uid, ids, lot, context)
                vivas = self._get_gall_pre(cr, uid, ids, date, lot, context)
                dayly_info = self._get_dayly_info(cr, uid, ids, date, lot, context)
                feed_info = self._get_feed_info(cr, uid, ids, date, lot, locations[0], context)
                egg_info = self._get_egg_info(cr, uid, ids, date, lot, locations[0], dayly_info[0], context)
                
                result = {'date':redate, 
                          'day':date, 
                          'prodlot_id':lot, 
                          'bajas_gall':gall_baj, 
                          'week_age':week_age, 
                          'nave':locations[0], 
                          'granja':locations[1], 
                          'existencias_gall':vivas, 
                          'egg_weight':dayly_info[0], 
                          'water_consum':dayly_info[1], 
                          'max_temp':dayly_info[2], 
                          'min_temp':dayly_info[3],
                          'feed_entries':feed_info[0],
                          'feed_inv':feed_info[2],
                          'egg_prod_qty':egg_info[0],
                          'egg_prod_kg':egg_info[1],
                          'egg_sale_qty':egg_info[2],
                          'egg_sale_kg':egg_info[3],
                          'all_egg_qty':egg_info[4]}
                
                exists = self.search(cr, uid, [('date', '=', date), ('prodlot_id', '=', lot)])
                if exists:
                    self.write(cr, uid, exists, result)
                else:    
                    self.create(cr, uid, result) 
                cr.commit()
                
        print "END!!!!  " + time.strftime('%H:%M:%S')
        return True
    
dayly_production()
