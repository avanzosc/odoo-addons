# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc, OpenERP Professional Services   
#    Copyright (C) 2010-2011 Avanzosc S.L (http://www.avanzosc.com). All Rights Reserved
#    
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

class estirpe_estirpe(osv.osv):
    
    _name = 'estirpe.estirpe'
        
    _columns = {
                'product_id':fields.many2one('product.product', 'Estirpe', required=True),
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
                'product_id':fields.many2one('product.product', 'Estirpe'),
                'lines':fields.one2many('estirpe.line', 'previ_id', 'Lines', required=True),
                'cre_date':fields.date('Create date', readonly=True),                
                }
    _defaults = {
                 'cre_date':lambda *a:time.strftime('%Y-%m-%d'),
                 } 
    
    def onchange_lot(self, cr, uid, fields, lot, context=None):
        res = {}
        if lot:
            lote = self.pool.get('stock.production.lot').browse(cr,uid,lot)            
            product = lote.product_id       
            res = {
                'product_id': product.id,
                }
        return {'value': res} 
        
    def load_data(self, cr, uid, ids, context=None):               
        previ= self.pool.get('estirpe.lot.prevision').browse(cr, uid, ids, context)[0]
        self.pool.get('estirpe.lot.prevision').write(cr, uid, [previ.id],{ 'cre_date': time.strftime('%Y-%m-%d')})
        startdate = time.strftime('%Y-%m-%d')
        lote = previ.lot   
        lines=previ.lines         
        product = lote.product_id  
        estirpe_ids = self.pool.get('estirpe.estirpe').search(cr,uid, [('product_id', '=', product.id)])
        if lines:
            raise osv.except_osv(_('Caution!'),_('Previsions are already loaded.'))       
        else:
            if estirpe_ids:
                for id in estirpe_ids:
                    est = self.pool.get('estirpe.estirpe').browse(cr, uid, id)
                    age_day = est.age -17
                    get_date = datetime.strptime(startdate,"%Y-%m-%d") + relativedelta(weeks=1)
        
                    line_id = self.pool.get('estirpe.line').create(cr,uid,{
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
                          
                    })  
                    startdate=datetime.strftime(get_date,"%Y-%m-%d")
            else: 
                raise osv.except_osv(_('Error!'),_('There is no lineage asigned for this lot.'))       
        return previ.id  
        
estirpe_lot_prevision()

class estirpe_line(osv.osv):
    
    _name = 'estirpe.line'    
    _columns = {
                'product_id':fields.many2one('product.product', 'Estirpe', required=True),
                'age': fields.integer('Edad', size=10, help="Se mide en semanas", readonly=True),
                'state_cod':fields.many2one('estado.productivo','Estado Pro.', readonly=True),
                'baj_acu':fields.float('Baj. acu.(%)', digits = (10,3), readonly=True),
                'baj_sem':fields.float('Baj. sem.(%)', digits = (10,3), readonly=True),
                'peso_gall':fields.float('Peso Gallina', digits = (10,3), help="Se mide en Kg.", readonly=True),
                'cons_sem_gr':fields.integer('Con. sem.',size=10, help="Se mide en gr.", readonly=True),
                'hue_prod':fields.float('Hue. pro.(%)', digits = (10,3), readonly=True),
                'peso_medio_hue_gr':fields.float('Peso me. hue.', digits = (10,3), help="Se mide en gr.", readonly=True),
                'previ_id':fields.many2one('estirpe.lot.prevision', 'Prevision', required=True),
                'date':fields.date('Date'),
                'baj_sem_real':fields.float('Baj. sem.(%)', digits = (10,3), required=True),  
                'cons_sem_real':fields.integer('Con. sem.',size=10, help="Se mide en gr.", required=True),
                'baj_acu_real':fields.float('Baj. acu.(%)', digits = (10,3), required=True),
                'hue_prod_real':fields.float('Hue. pro.(%)', digits = (10,3), required=True),
                'peso_hue_real':fields.float('Peso hue.', digits = (10,3), help="Se mide en gr.", required=True)    
               }
estirpe_line()






