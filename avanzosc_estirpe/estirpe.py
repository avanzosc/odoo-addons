
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

class estado_productivo(osv.osv):    
    _name = 'estado.productivo'
    
    _columns = {
                'name':fields.char('Nombre', size=20, required=True),
                'cod':fields.char('Cod.', size=10),
                }   
estado_productivo()

class estandar_estirpe(osv.osv):
    _name = 'estandar.estirpe'
    
    _columns = {
                'name':fields.char('Nombre', size=20, required=True),
                'cod':fields.char('Cod.', size=10),                
                }
estandar_estirpe()

class estirpe_estirpe(osv.osv):
    
    _name = 'estirpe.estirpe'
        
    _columns = {
                'product_id':fields.many2one('estandar.estirpe','Estándar', required=True),
                'age': fields.integer('Edad', size=10, help="Se mide en semanas", required=True),
                'state_cod':fields.many2one('estado.productivo','Estado Productivo'),
                'baj_acu':fields.float('Bajas acumuladas(%)', digits = (10,3)),
                'baj_sem':fields.float('Bajas semanales(%)', digits = (10,3)),
                'peso_gall':fields.float('Peso Gallina', digits = (10,3), help="Se mide en Kg."),
                'cons_dia_gr':fields.integer('Consumo por dia',size=10, help="Se mide en gr."),
                'hue_prod':fields.float('Huevos produccion(%)', digits = (10,3)),
                'peso_medio_hue_gr':fields.float('Peso medio huevo', digits = (10,3), help="Se mide en gr."),                
                } 
    _defaults = {  
                'state_cod': lambda self,cr,uid,c: self.pool.get('estado.productivo').search(cr, uid, [('name', '=', 'Prepuesta')])[0],
                } 
 
estirpe_estirpe()

class estirpe_lot_prevision(osv.osv):
    _name = 'estirpe.lot.prevision'
    
    _columns = {
                'lot':fields.many2one('stock.production.lot', 'Lot', required=True),
                'product_id':fields.many2one('product.product', 'Producto'),
                'estandar_id':fields.many2one('estandar.estirpe', 'Estándar', required=True),
                'lines':fields.one2many('estirpe.line', 'previ_id', 'Lines'),
                'cre_date':fields.related('lot','date', type="date", relation="stock.production.lot", string="Create date", store=True, readonly=True),
                'nac_date':fields.date('Birth date', required=True),
                'date':fields.date('Load date'),
                'location1':fields.many2one('stock.location', 'Ubi. Bajas', required=True),
                'location2':fields.many2one('stock.location', 'Nave', required=True),
                'location3':fields.many2one('stock.location', 'Ubi. Consumo'),

                } 
    
    def onchange_lot(self, cr, uid, ids, lot, context=None):
        res = {}
        lots=self.pool.get('estirpe.lot.prevision').search(cr,uid,[('lot','=',lot)])
        if lots:
            raise osv.except_osv(_('Error!'),_('Already exists prevision control for this lot.'))       
        if lot:            
            lote = self.pool.get('stock.production.lot').browse(cr,uid,lot)            
            product = lote.product_id       
            res = {
                'product_id': product.id,
                }
        return {'value': res} 
    
    
    def onchange_date(self, cr, uid, ids, date, estandar, context=None):
        res={}
        if date:
            if estandar: 
                estandares = self.pool.get('estirpe.estirpe').search(cr, uid, [('product_id', '=', estandar)])
                week = self.pool.get('estirpe.estirpe').browse(cr, uid, estandares[0]).age  
            else:
                week = 18
         
            load_date=datetime.strptime(date,"%Y-%m-%d") + relativedelta(weeks=week)
            res={
                 'date': datetime.strftime(load_date,"%Y-%m-%d")
                 }
        return {'value': res}
             
            
                        
    def load_data(self, cr, uid, ids, context=None):               
        
        previ= self.pool.get('estirpe.lot.prevision').browse(cr, uid, ids, context)[0]        
        
        if not previ.date:
            res = previ.onchange_date(previ.nac_date, previ.estandar_id.id)
            self.pool.get('estirpe.lot.prevision').write(cr, uid, [previ.id],{'date':res['value']['date']})
            finalDate = res['value']['date']
        else:
            finalDate = previ.date
        startdate=time.strftime('%Y-%m-%d', time.strptime(finalDate, '%Y-%m-%d'))              
        
        lote = previ.lot
        self.pool.get('estirpe.lot.prevision').write(cr, uid, [previ.id], {'cre_date': lote.date}) 
        
        estandar = previ.estandar_id.id
        estirpe_ids = self.pool.get('estirpe.estirpe').search(cr,uid, [('product_id', '=', estandar)])
        
        lot = previ.lot
        lines = previ.lines         
        product = lote.product_id  
        
        if lines:  
            first_id=lines[0].id          
            last_id = lines[0].id
            for line in lines:
                if ((line.baj_sem_real > 0.0) or (line.cons_sem_real > 0) or (line.baj_acu_real > 0.0) or (line.hue_prod_real > 0.0) or (line.peso_hue_real > 0.0)):
                    last_id = line.id
            
            last_date=time.strftime('%Y-%m-%d')
            last_age = 18
            if (last_id == first_id):
                for line in lines:
                    if (line.id==first_id):
                        if not ((line.baj_sem_real > 0.0) or (line.cons_sem_real > 0) or (line.baj_acu_real > 0.0) or (line.hue_prod_real > 0.0) or (line.peso_hue_real > 0.0)):
                            self.pool.get('estirpe.line').unlink(cr, uid, [line.id])
                            startdate = previ.date
                            get_date = datetime.strptime(startdate, '%Y-%m-%d') + relativedelta(weeks=-1)
                            last_date=datetime.strftime(get_date,"%Y-%m-%d") 
                        else:
                             last_date = line.date
                             last_age = line.age 
                    else:
                        if (line.id > last_id):
                            self.pool.get('estirpe.line').unlink(cr, uid, [line.id]) 
            else:
                for line in lines:
                    if (line.id > last_id):
                        self.pool.get('estirpe.line').unlink(cr, uid, [line.id])
                last_line = self.pool.get('estirpe.line').browse(cr, uid, last_id)
                last_date = last_line.date
                last_age = last_line.age  
                
            if estirpe_ids:                
                startdate = last_date                
                for id in estirpe_ids: 
                    est = self.pool.get('estirpe.estirpe').browse(cr, uid, id)
                    if est.age > last_age:
                        get_date = datetime.strptime(startdate,"%Y-%m-%d") + relativedelta(weeks=1)
            
                        line_id = self.pool.get('estirpe.line').create(cr,uid,{
                              'estandar_id':est.product_id.id,
                              'lot':lot.id,
                              'product_id':product.id,                                                
                              'date':get_date,                                                                   
                              'age' : est.age,
                              'state_cod' : est.state_cod.id,
                              'baj_acu':est.baj_acu,
                              'baj_sem':est.baj_sem,
                              'peso_gall':est.peso_gall,
                              'cons_sem_gr':est.cons_dia_gr * 7,
                              'hue_prod':est.hue_prod,
                              'peso_medio_hue_gr':est.peso_medio_hue_gr,
                              'previ_id':previ.id,
                              'baj_sem_real':0.0,
                              'cons_sem_real':0,
                              'baj_acu_real':0.0,
                              'hue_prod_real':0.0,
                              'peso_hue_real':0.0,
                              'gal_pres':0.0,
                        })  
                        startdate=datetime.strftime(get_date,"%Y-%m-%d")               
        else:
            if estirpe_ids:                
                get_date = datetime.strptime(startdate, '%Y-%m-%d') + relativedelta(weeks=-1)
                startdate=datetime.strftime(get_date,'%Y-%m-%d')              
                for id in estirpe_ids:
                    est = self.pool.get('estirpe.estirpe').browse(cr, uid, id)
                    get_date = datetime.strptime(startdate,"%Y-%m-%d") + relativedelta(weeks=1)
        
                    line_id = self.pool.get('estirpe.line').create(cr,uid,{
                          'estandar_id':est.product_id.id,  
                          'lot':lot.id,                                           
                          'product_id':product.id,                                                
                          'date':get_date,                                                                   
                          'age' : est.age,
                          'state_cod' : est.state_cod.id,
                          'baj_acu':est.baj_acu,
                          'baj_sem':est.baj_sem,
                          'peso_gall':est.peso_gall,
                          'cons_sem_gr':est.cons_dia_gr * 7,
                          'hue_prod':est.hue_prod,
                          'peso_medio_hue_gr':est.peso_medio_hue_gr,
                          'previ_id':previ.id,
                          'baj_sem_real':0.0,
                          'cons_sem_real':0,
                          'baj_acu_real':0.0,
                          'hue_prod_real':0.0,
                          'peso_hue_real':0.0,
                          'gal_pres':0.0,
                    })  
                    startdate=datetime.strftime(get_date,"%Y-%m-%d")
            else: 
                raise osv.except_osv(_('Error!'),_('There is no lineage asigned for this lot.'))       
        return previ.id  
    
    def get_last_inventories_qty(self, cr, uid, ids, date, location, context=None ):
        com_id = self.pool.get('res.company').search(cr,uid,[])
        compa = self.pool.get('res.company').browse(cr, uid, com_id[0])
        feed_cat = compa.cat_feed_ids
        
        last = datetime.strptime(date,"%Y-%m-%d") + relativedelta(days=6)
        date = datetime.strftime(last,"%Y-%m-%d")
        
        location_list = self.pool.get('stock.location').search(cr,uid, [('location_id', '=', location.location_id.id)])
        first_qty = 0.0
        last_qty = 0.0        
        if not feed_cat:
            raise osv.except_osv(_('Error!'),_('There is no feed category especified for this company.'))
        else:
            lines = []
            inventory_list = []
            for cat in feed_cat:
                lines_list = self.pool.get('stock.inventory.line').search(cr,uid,[('product_id.product_tmpl_id.categ_id', '=', cat.id), ('location_id', 'in', location_list)])
                for line in lines_list:
                    lines.append(line)
            for inv_line in lines:
                if inv_line:
                    inv_line_obj = self.pool.get('stock.inventory.line').browse(cr,uid,inv_line)
                    inv_obj = self.pool.get('stock.inventory').browse(cr,uid,inv_line_obj.inventory_id)
                    if inv_line_obj.inventory_id.date <= date:
                        inventory_list.append(inv_line_obj.inventory_id)
            if inventory_list != []:            
                last_date = inventory_list[0].date
                min_date = inventory_list[0].date
                last_inv = inventory_list[0]
                min_inv = inventory_list[0]
                for inv in inventory_list:
                    inv_obj = self.pool.get('stock.inventory').browse(cr, uid, inv)
                  
                    if inv.date >= last_date:
                        last_date = inv.date
                        last_inv = inv
                    elif inv.date < min_date:
                        min_date = inv.date
                        min_inv = inv
                if inventory_list.__len__() > 1:
                    first_date = min_date
                    first_inv = min_inv
                    for inv in inventory_list:
                        inv_obj = self.pool.get('stock.inventory').browse(cr, uid, inv)
                        if ((inv.date < last_date) and (inv.date >= first_date)):
                            first_date = inv.date
                            first_inv = inv   
                    inv_line_first = self.pool.get('stock.inventory.line').search(cr,uid,[('inventory_id','=',first_inv.id), ('product_id.product_tmpl_id.categ_id', '=', cat.id), ('location_id', 'in', location_list)])
                    first_qty = 0.0
                    for line in inv_line_first:
                        first_qty = first_qty + self.pool.get('stock.inventory.line').browse(cr, uid, line).product_qty
                else:
                    first_qty = 0.0
                                
                inv_line_last = self.pool.get('stock.inventory.line').search(cr,uid,[('inventory_id','=',last_inv.id), ('product_id.product_tmpl_id.categ_id', '=', cat.id), ('location_id', 'in', location_list)])
                last_qty = 0.0
                for line in inv_line_last:
                    last_qty = last_qty + self.pool.get('stock.inventory.line').browse(cr, uid, line).product_qty
                                
                qty_list = []
                qty_list.append(first_qty)
                qty_list.append(last_qty)
            else:
                raise osv.except_osv(_('Error!'),_('There is no feed inventory created before %s in %s'%(date, location.name)))
        return qty_list      
                    
       
    def calc_week (self, cr, uid, ids, context=None):
        compa = self.pool.get('res.company').browse(cr, uid, ids[0])
        feed_cat = compa.cat_feed_ids
        egg_cat = compa.cat_egg_ids
        chicken_cat = compa.cat_chicken_ids
#        if not (feed_cat and egg_cat and chicken_cat):
#            raise osv.except_osv(_('Error!'),_('There is no default category especified for this company.'))
#        else:
        cont_prod = self.browse(cr,uid,ids)[0]
        if cont_prod.location1:
            ubi_bajas = cont_prod.location1 
        if cont_prod.location2:
            ubi_nave = cont_prod.location2
        if cont_prod.location3:
            ubi_prod = cont_prod.location3
        else:
            ubi_prod = cont_prod.location2
        lot = cont_prod.lot
        if not cont_prod.lines:
            raise osv.except_osv(_('Error!'),_('You have to load previsions!'))     
        ini_id = self.pool.get('stock.move').search(cr,uid,[('location_dest_id','=', ubi_nave.id),('prodlot_id','=',lot.id)])
        if not ini_id:
            raise osv.except_osv(_('Error!'),_('This lot is not in the specified location!'))
        else:
            gall_ini=self.pool.get('stock.move').browse(cr,uid,ini_id[0]).product_qty
        last = datetime.strptime(time.strftime('%Y-%m-%d'),"%Y-%m-%d") + relativedelta(days=-6)
        pre_date = datetime.strftime(last,"%Y-%m-%d")
        lines = self.pool.get('estirpe.line').search(cr,uid,[('lot','=',lot.id),('date','<', pre_date)])
        if lines:
            line_id=self.pool.get('estirpe.line').browse(cr,uid,lines[0])
            first_id = line_id.id          
            last_id = line_id.id
            for line in lines:
                line_obj=self.pool.get('estirpe.line').browse(cr,uid,line)
                if ((line_obj.baj_sem_real != 0.0) or (line_obj.cons_sem_real != 0) or (line_obj.baj_acu_real != 0.0) or (line_obj.hue_prod_real != 0.0) or (line_obj.peso_hue_real != 0.0) or (line_obj.gal_pres != 0.0)):
                    last_id = line_obj.id
            for line in lines:
                
                line_obj=self.pool.get('estirpe.line').browse(cr,uid,line)
                if line_obj.id > last_id:
                    start_date = line_obj.date
                    if not ((line_obj.baj_sem_real!=0.0) or (line_obj.baj_acu_real!=0.0) or (line_obj.cons_sem_real!=0) or (line_obj.hue_prod_real!=0.0) or (line_obj.peso_hue_real!=0.0) or (line_obj.gal_pres != 0.0)):
                        gall_act = self.calc_gall_pre(cr, uid, ids, start_date, lot, ubi_nave,ubi_bajas)
                        hue_sem = self.calc_huevos_semanal(cr, uid, ids, start_date, ubi_nave)
                        pienso_sem = self.calc_pienso_semanal(cr, uid, ids, start_date, ubi_prod)
                        self.get_last_inventories_qty(cr, uid, ids, start_date, ubi_prod)
                        baj_sem=self.calc_baj_sema(cr,uid,ids,start_date, lot, ubi_nave, ubi_bajas)
                        baj_acu = 100 - ((gall_act / gall_ini)*100)
                        peso_medio = self.calc_peso_medio(cr, uid, ids, start_date, lot)
                        hue_prod = round(((hue_sem / (gall_act *7))*100),3)
                        cons_sem = (pienso_sem/(gall_act*7))*1000
                        self.pool.get('estirpe.line').write(cr,uid,[line],{'baj_sem_real':baj_sem,'baj_acu_real':baj_acu,'cons_sem_real':cons_sem,'hue_prod_real':hue_prod,'peso_hue_real':peso_medio, 'gal_pres':gall_act})
            return ids[0]
    
    
    def calc_gall_pre(self, cr,uid, ids, start_date, lot, ubi,ubi_baja):
        move_obj = self.pool.get('stock.move')
        last = datetime.strptime(start_date,"%Y-%m-%d") + relativedelta(days=6)
        last_date = datetime.strftime(last,"%Y-%m-%d")
        moves_neg = move_obj.search(cr,uid,[('prodlot_id','=', lot.id),('date','<=', last_date),('date','>=', start_date), ('location_id','=',ubi.id),('state','=','done')])
        moves_pos = move_obj.search(cr,uid,[('prodlot_id','=', lot.id),('date','<=', last_date),('location_dest_id','=',ubi.id),('state','=','done')])
        cant = 0
        for move_neg in moves_neg:
            move_br = move_obj.browse(cr,uid,move_neg)
            cant = cant - move_br.product_qty
        for move_pos in moves_pos:
            move_br = move_obj.browse(cr,uid,move_pos)
            cant = cant + move_br.product_qty
        return cant
    
    
    def calc_peso_medio(self, cr, uid, ids, start_date, lot):
        peso=0
        kont = 0
        last = datetime.strptime(start_date,"%Y-%m-%d") + relativedelta(days=6)
        date = start_date
        last_date = datetime.strftime(last,"%Y-%m-%d")
        while date <= last_date:
            dayly_part = self.pool.get('dayly.part').search(cr,uid,[('date','=',date),('prodlot_id','=', lot.id)])
            if dayly_part:
                part = self.pool.get('dayly.part').browse(cr,uid,dayly_part[0])
                peso = peso + part.eggs_weigth
                kont= kont + 1
              
            next_date = datetime.strptime(date, "%Y-%m-%d") + relativedelta(days=1)
            date=datetime.strftime(next_date,"%Y-%m-%d")
        if kont== 0:
            peso = 0
        else:
            peso = peso / kont
        peso = round(peso, 3)
        return peso
    
    def calc_baj_sema(self,cr,uid,ids,start_date,lot,ubi, ubi_baja):
        last = datetime.strptime(start_date,"%Y-%m-%d") + relativedelta(days=6)
        last_date = datetime.strftime(last,"%Y-%m-%d")
        moves = self.pool.get('stock.move').search(cr,uid,[('prodlot_id','=', lot.id),('date','<=', last_date),('date','>=',start_date), ('location_id','=',ubi.id),('location_dest_id','=',ubi_baja.id)])
        cant = 0
        if moves:
            for move in moves:
                move_br = self.pool.get('stock.move').browse(cr,uid,move)
                cant = cant + move_br.product_qty
        ini_id = self.pool.get('stock.move').search(cr,uid,[('location_dest_id','=', ubi.id),('prodlot_id','=',lot.id)])[0]
        gall_ini = self.pool.get('stock.move').browse(cr,uid,ini_id).product_qty
        baj_sem = (cant / gall_ini) *100
        baj_sem=round(baj_sem,3)
        return baj_sem
    
    
    def calc_pienso_semanal(self, cr, uid, ids, start_date, ubi):
        last = datetime.strptime(start_date,"%Y-%m-%d") + relativedelta(days=6)
        last_date = datetime.strftime(last,"%Y-%m-%d")
        qty_list = self.get_last_inventories_qty(cr, uid, ids, last_date, ubi)
        
        inventory_loc = self.pool.get('stock.location').search(cr,uid,[('usage','=','inventory')])
        com_id = self.pool.get('res.company').search(cr,uid,[])
        compa = self.pool.get('res.company').browse(cr, uid, com_id[0])
        feed_cat = compa.cat_feed_ids        
                
        ubi_list = self.pool.get('stock.location').search(cr,uid,[('location_id','=',ubi.location_id.id)])
        if not feed_cat:
            raise osv.except_osv(_('Error!'),_('There is no feed category especified for this company.'))
        else:
            mov_piens = []
            for cat in feed_cat:
                lines_list = self.pool.get('stock.move').search(cr,uid,[('location_dest_id','in',ubi_list),('product_id.product_tmpl_id.categ_id', '=', cat.id),('date','>=',start_date),('date','<=', last_date)])
                for line in lines_list:
                    line_obj = self.pool.get('stock.move').browse(cr,uid,line)
                    if not line_obj.location_id.id in inventory_loc:
                        mov_piens.append(line)
            mov_piens_out = []
            for cat in feed_cat:
                lines_list = self.pool.get('stock.move').search(cr,uid,[('location_id','in',ubi_list),('product_id.product_tmpl_id.categ_id', '=', cat.id),('date','>=',start_date),('date','<=', last_date)])
                for line in lines_list:
                    line_obj = self.pool.get('stock.move').browse(cr,uid,line)
                    if not line_obj.location_dest_id.id in inventory_loc: 
                        mov_piens_out.append(line)
        cant=0
        if mov_piens:
            for move in mov_piens:
               move_pi = self.pool.get('stock.move').browse(cr,uid,move)
               cant = cant + move_pi.product_qty
        if mov_piens_out:
            for move in mov_piens_out:
               move_pi = self.pool.get('stock.move').browse(cr,uid,move)
               cant = cant - move_pi.product_qty
        cant = cant + qty_list[0] - qty_list[1]
        pienso = cant
        return pienso
    
    
    def calc_huevos_semanal(self, cr,uid,ids,start_date,ubi):
        
        last = datetime.strptime(start_date,"%Y-%m-%d") + relativedelta(days=6)
        last_date = datetime.strftime(last,"%Y-%m-%d")
        com_id = self.pool.get('res.company').search(cr,uid,[])
        compa = self.pool.get('res.company').browse(cr, uid, com_id[0])
        egg_loc = self.pool.get('stock.location').search(cr,uid,[('egg_production', '=', True)])
        egg_cat = compa.cat_egg_ids
        if not egg_cat:
            raise osv.except_osv(_('Error!'),_('There is no egg category especified for this company.'))
        else:
            mov_hue = []
            for cat in egg_cat:
                mov_hue_list = self.pool.get('stock.move').search(cr,uid,[('location_id', 'in', egg_loc),('location_dest_id','=',ubi.id),('product_id.product_tmpl_id.categ_id', '=', cat.id),('date','>=',start_date),('date','<=', last_date)])

                for line in mov_hue_list:
                    mov_hue.append(line)
        cant=0
        if mov_hue:
            for move in mov_hue:
               move_hu = self.pool.get('stock.move').browse(cr,uid,move)
               cant = cant + move_hu.product_qty
        huevos = cant
        return huevos
    
    
    def calc_all(self, cr, uid, ids, context=None):
        compa = self.pool.get('res.company').browse(cr, uid, ids[0])
        feed_cat = compa.cat_feed_ids
        egg_cat = compa.cat_egg_ids
        chicken_cat = compa.cat_chicken_ids
        cont_prod = self.browse(cr,uid,ids)[0]
        if cont_prod.location1:
            ubi_bajas = cont_prod.location1 
        if cont_prod.location2:
            ubi_nave = cont_prod.location2
        if cont_prod.location3:
            ubi_prod = cont_prod.location3
        else:
            ubi_prod = cont_prod.location2
        lot = cont_prod.lot
        if not cont_prod.lines:
            raise osv.except_osv(_('Error!'),_('You have to load previsions!'))     
        ini_id = self.pool.get('stock.move').search(cr,uid,[('location_dest_id','=', ubi_nave.id),('prodlot_id','=',lot.id)])
        if not ini_id:
            raise osv.except_osv(_('Error!'),_('This lot is not in the specified location!'))
        else:
            gall_ini=self.pool.get('stock.move').browse(cr,uid,ini_id[0]).product_qty
        last = datetime.strptime(time.strftime('%Y-%m-%d'),"%Y-%m-%d") + relativedelta(days=-6)
        pre_date = datetime.strftime(last,"%Y-%m-%d")
        lines = self.pool.get('estirpe.line').search(cr,uid,[('lot','=',lot.id),('date','<', pre_date)])
        if lines:
            for line in lines:
                line_obj=self.pool.get('estirpe.line').browse(cr,uid,line)
                start_date = line_obj.date
            
                gall_act = self.calc_gall_pre(cr, uid, ids, start_date, lot, ubi_nave,ubi_bajas)
                hue_sem = self.calc_huevos_semanal(cr, uid, ids, start_date, ubi_nave)
                pienso_sem = self.calc_pienso_semanal(cr, uid, ids, start_date, ubi_prod)
            
                baj_sem=self.calc_baj_sema(cr,uid,ids,start_date, lot, ubi_nave, ubi_bajas)
                baj_acu = 100 - ((gall_act / gall_ini)*100)
                peso_medio = self.calc_peso_medio(cr, uid, ids, start_date, lot)
                hue_prod = round(((hue_sem / (gall_act *7))*100),3)
                cons_sem = (pienso_sem/(gall_act*7))*100
                self.pool.get('estirpe.line').write(cr,uid,[line],{'baj_sem_real':baj_sem,'baj_acu_real':baj_acu,'cons_sem_real':cons_sem,'hue_prod_real':hue_prod,'peso_hue_real':peso_medio, 'gal_pres':gall_act})
            return ids[0]   
        
     
     
     
    def calculate_conf_week(self, cr, uid, ids, context=None):
        if context is None: context = {}
        estlot = self.pool.get('estirpe.lot.prevision').browse(cr,uid,ids)[0]
        mod_obj = self.pool.get('ir.model.data')
        form_res1 = mod_obj.get_object_reference(cr, uid, 'avanzosc_estirpe', 'confirm_calculate_form1')
        form_id1 = form_res1 and form_res1[1] or False
        selec = self.pool.get("confirm.calculate").create(cr, uid, {'lot':estlot.lot.id }, context=dict(context, active_ids=ids))
        return {
            'name':_("Confirm"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'confirm.calculate',
            'res_id': selec,
            'views': [(form_id1, 'form')],
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': dict(context, active_ids=ids) 
            }     
        
        
    def calculate_conf_all(self, cr, uid, ids, context=None):
        if context is None: context = {}
       
        estlot = self.pool.get('estirpe.lot.prevision').browse(cr,uid,ids)[0]
        
        mod_obj = self.pool.get('ir.model.data')
        form_res1 = mod_obj.get_object_reference(cr, uid, 'avanzosc_estirpe', 'confirm_calculate_form2')
        form_id1 = form_res1 and form_res1[1] or False
        selec = self.pool.get("confirm.calculate").create(cr, uid, {'lot':estlot.lot.id }, context=dict(context, active_ids=ids))
        return {
            'name':_("Confirm"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'confirm.calculate',
            'res_id': selec,
            'views': [(form_id1, 'form')],
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': dict(context, active_ids=ids) 
            }     
    
estirpe_lot_prevision()

class estirpe_line(osv.osv):
    
    _name = 'estirpe.line'    
    _columns = {
                'estandar_id':fields.many2one('estandar.estirpe', 'Estándar', readonly=True),
                'age': fields.integer('Edad', size=10, help="Se mide en semanas", readonly=True),
                'state_cod':fields.many2one('estado.productivo','Estado Pro.', readonly=True),
                'gal_pres':fields.float('Gall pres.', digits = (10,3), required=True),
                'baj_acu':fields.float('Baj. acu.', digits = (10,3), readonly=True),
                'baj_sem':fields.float('Baj. sem.', digits = (10,3), readonly=True),
                'peso_gall':fields.float('Peso Gallina', digits = (10,3), help="Se mide en Kg.", readonly=True),
                'cons_sem_gr':fields.integer('Con. sem.',size=10, help="Se mide en gr.", readonly=True),
                'hue_prod':fields.float('Hue. pro.', digits = (10,3), readonly=True),
                'peso_medio_hue_gr':fields.float('Peso me. hue.', digits = (10,3), help="Se mide en gr.", readonly=True),
                'previ_id':fields.many2one('estirpe.lot.prevision', 'Prevision'),
                'lot':fields.many2one('stock.production.lot', 'Lot'),
                'date':fields.date('Date', readonly=True),
                'baj_sem_real':fields.float('%Baj. sem.', digits = (10,3), required=True),  
                'cons_sem_real':fields.integer('Con. sem.',size=10, help="Se mide en gr.", required=True),
                'baj_acu_real':fields.float('%Baj. acu.', digits = (10,3), required=True),
                'hue_prod_real':fields.float('%Hue. pro.', digits = (10,3), required=True),
                'peso_hue_real':fields.float('Peso hue.', digits = (10,3), help="Se mide en gr.", required=True)    
               }
estirpe_line()

class selection_mode(osv.osv):
    _name = 'selection.mode'
    
    _columns = {
                'estandar':fields.many2one('estandar.estirpe', 'Estándar', required=True),
                'birth_date':fields.date('Lot birth date', required=True),
                'date':fields.date('Prevision start date'),
                'location1':fields.many2one('stock.location', 'Ubi. Bajas', required=True),
                'location2':fields.many2one('stock.location', 'Nave', required=True),
                'location3':fields.many2one('stock.location', 'Ubi. Consumo'),
                'lot':fields.many2one('stock.production.lot', 'Lot', required=True),
                }
    
    def onchange_date(self, cr, uid, ids, date, estandar, context=None):
        res={}
        if date:
            if estandar: 
                estandares = self.pool.get('estirpe.estirpe').search(cr, uid, [('product_id', '=', estandar)])
                week = self.pool.get('estirpe.estirpe').browse(cr, uid, estandares[0]).age  
            else:
                week = 18
         
            load_date=datetime.strptime(date,"%Y-%m-%d") + relativedelta(weeks=week)
            res={
                 'date': datetime.strftime(load_date,"%Y-%m-%d")
                 }
        return {'value': res}
    
    def create_prevision(self, cr, uid, ids, context=None):
        if context is None: context = {}        
        selec = self.pool.get("selection.mode").browse(cr,uid,ids)[0]
        lot = selec.lot.id
        estirpe = self.pool.get("estirpe.lot.prevision").search(cr,uid,[('lot','=',lot)])
        
        if estirpe:
            prev = estirpe[0]
            self.pool.get("estirpe.lot.prevision").write(cr, uid, [prev], {'estandar_id':selec.estandar.id})
        else:
            if not selec.location3:
                location3 = selec.location2.id
            else:
                location3 = selec.location3.id
            prev = self.pool.get("estirpe.lot.prevision").create(cr, uid, {'nac_date':selec.birth_date,'date': selec.date, 'estandar_id':selec.estandar.id, 'lot':selec.lot.id, 'product_id':selec.lot.product_id.id, 'location1':selec.location1.id, 'location2':selec.location2.id, 'location3':location3 }, context=dict(context, active_ids=ids))
        
        data = self.pool.get('estirpe.lot.prevision').browse(cr,uid,prev)
        data.load_data()
       
        
        mod_obj = self.pool.get('ir.model.data')
        form_res = mod_obj.get_object_reference(cr, uid, 'avanzosc_estirpe', 'stirpe_lot_prevision_form')
        form_id = form_res and form_res[1] or False
        tree_res = mod_obj.get_object_reference(cr, uid, 'avanzosc_estirpe', 'stirpe_lot_prevision_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
#            'name':_("Prevision"),
#            'view_mode': 'form',
#            'view_type': 'form,tree',
#            'view_id': False,
#            'res_model': 'estirpe.lot.prevision',
#            'res_id': data.id,
#            'views':[(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window.close()',
#            'nodestroy': True,
#            'domain': '[]',
#            'context': dict(context, active_ids=ids) 
            }
            
            
            
    
selection_mode()

class stock_production_lot(osv.osv):
        
    _inherit = 'stock.production.lot'
    
    _columns = {
                'gallina':fields.boolean('Es gallina'),
                'lines':fields.one2many('estirpe.line', 'lot', 'Lines'),
                }

    def is_pro_name(self, cr, uid, ids, product_id, context=None):
        res={}
       	if product_id:
            com_id = self.pool.get('res.company').search(cr,uid,[])
    	    compa = self.pool.get('res.company').browse(cr, uid, ids[0])
    	    gall_cat = compa.cat_chicken_ids
    	    if not gall_cat:
    	        raise osv.except_osv(_('Error!'),_('There is no chicken category especified for this company.'))
    	    else:
    	        if product_id:
    	            pro = self.pool.get('product.product').browse(cr,uid,product_id)                 
    	            if (product_id.product_tmpl_id.categ_id in gall_cat):
    	                res = {
    	                       'gallina':True
    	                       }
    	            else:
    	                res = {
    	                       'gallina':False
    	                       }
        return {'value':res}
    
    
    def create_prevision(self, cr, uid, ids, context=None):
        if context is None: context = {}
       
        lot = self.pool.get('stock.production.lot').browse(cr,uid,ids)[0].id
        date =  time.strftime('%Y-%m-%d')
        est_lot = self.pool.get('estirpe.lot.prevision').search(cr, uid, [('lot','=',lot)])
        
        mod_obj = self.pool.get('ir.model.data')
        form_res1 = mod_obj.get_object_reference(cr, uid, 'avanzosc_estirpe', 'selection_mode_form')
        form_id1 = form_res1 and form_res1[1] or False
        form_res2 = mod_obj.get_object_reference(cr, uid, 'avanzosc_estirpe', 'selection_mode_form2')
        form_id2 = form_res2 and form_res2[1] or False
        
        
        if est_lot:
            lot_pre=self.pool.get('estirpe.lot.prevision').browse(cr,uid,est_lot[0])
            selec = self.pool.get("selection.mode").create(cr, uid, {'birth_date':date, 'estandar':lot_pre.estandar_id.id, 'lot':lot }, context=dict(context, active_ids=ids))
            return {
                'name':_("Select options"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'selection.mode',
                'res_id': selec,
                'views': [(form_id2, 'form')],
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context': dict(context, active_ids=ids) 
                }     
        else:
            estand = self.pool.get('estandar.estirpe').search(cr,uid,[])[0]
            selec = self.pool.get("selection.mode").create(cr, uid, {'birth_date':date, 'estandar':estand, 'lot':lot }, context=dict(context, active_ids=ids))
            return {
                'name':_("Select options"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'selection.mode',
                'res_id': selec,
                'views': [(form_id1, 'form')],
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context': dict(context, active_ids=ids) 
        }
    
stock_production_lot()


class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    def _create_lot(self, cr, uid, ids, product_id, prefix=False):
        """ Creates production lot
        @return: Production lot id
        """
        com_id = self.pool.get('res.company').search(cr,uid,[])
        compa = self.pool.get('res.company').browse(cr, uid, com_id[0])
        gall_cat = compa.cat_chicken_ids
        if not gall_cat:
            raise osv.except_osv(_('Error!'),_('There is no chicken category especified for this company.'))
        else:
            pro_name = product_id.name
            if (product_id.product_tmpl_id.categ_id in gall_cat):
                ema=True
            else:
                ema=False
            prodlot_obj = self.pool.get('stock.production.lot')
            prodlot_id = prodlot_obj.create(cr, uid, {'prefix': prefix, 'product_id': product_id, 'gallina':ema})
        return prodlot_id
stock_move()

class confirm_calculate(osv.osv):
    _name = "confirm.calculate"    
    _columns = {
                'lot':fields.many2one('stock.production.lot', 'Lot', required=True)
                }
    
    
    def confirm_calculate_week(self, cr, uid, ids, context=None):
        if context is None: context = {}        
        selec = self.pool.get("confirm.calculate").browse(cr,uid,ids)[0]
        lot = selec.lot.id
        estirpe = self.pool.get("estirpe.lot.prevision").search(cr,uid,[('lot','=',lot)])
        prev = estirpe[0]
        data = self.pool.get('estirpe.lot.prevision').browse(cr,uid,prev)
        data.calc_week()
        return {
            'type': 'ir.actions.act_window.close()',
            }
        
    def confirm_calculate_all(self, cr, uid, ids, context=None):
        if context is None: context = {}        
        selec = self.pool.get("confirm.calculate").browse(cr,uid,ids)[0]
        lot = selec.lot.id
        estirpe = self.pool.get("estirpe.lot.prevision").search(cr,uid,[('lot','=',lot)])

        prev = estirpe[0]
        data = self.pool.get('estirpe.lot.prevision').browse(cr,uid,prev)
        data.calc_all()
        return {
            'type': 'ir.actions.act_window.close()',
            }
confirm_calculate()
