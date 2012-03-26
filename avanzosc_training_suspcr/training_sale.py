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

from osv import osv
from osv import fields
from datetime import datetime, timedelta  
from tools.translate import _
import decimal_precision as dp


class sale_order(osv.osv):
    _inherit = "sale.order"
    
    _columns = {
        'contact_id': fields.many2one('res.partner.contact', 'Contact', required=True),
        'subscription_id': fields.many2one('training.subscription', 'Subscription', ondelete='cascade', help='Select the subscription.'),
    }
    
    def onchange_partner_id(self, cr, uid, ids, part):
        #########################
        #OBJETOS#
        #####################################################
        partner_obj = self.pool.get('res.partner')
        #####################################################
        val = super(sale_order, self).onchange_partner_id(cr, uid, ids, part)['value']
        if part:
            partner = partner_obj.browse(cr, uid, part)
            if partner.address[0].job_ids[0].contact_id:
                val.update({'contact_id': partner.address[0].job_ids[0].contact_id.id})
        return {'value': val}
    
    def _insert_data_on_record(self, cr, uid, ids, linea, record_id):
        ###########################################################
        #orderline = liena
        #existe_expediente[0]  o new_training_record_obj = record_id
        ##################################################################
        training_record_line_obj = self.pool.get('training.record.line')
        ###################################################################
        res=[]
        
        valRecLine={
            'call':linea.call,
            'state':'recognized',
            'coursenum_id':linea.coursenum_id.id,
            'mark': 0,
            'date':datetime.now(),
            'name':linea.product_id.name,
            'session_id': linea.seance_id.id,
            'record_id':record_id,
            'tipology': linea.tipology,
            'type':"ordinary",
            'credits': linea.product_uom_qty,  
                    }
        
        if linea.call == 1:
            if linea.convalidate:
                valRecLine.update({
                    'state':'recognized',
                    'mark': 6,
                    'type':"ordinary",
                    })
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                res.append(new_training_record_line_obj) 
            else:
                valRecLine.update({
                    'state':'not_sub',
                    'mark': 0,
                    'type':"ordinary",
                    })
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                res.append(new_training_record_line_obj)
                valRecLine.update({
                    'call':linea.call+1,              
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                res.append(new_training_record_line_obj)
            
        if linea.call > 1:
            if linea.convalidate:
               valRecLine.update({
                    'state':'recognized',
                    'mark': 6,
                    'type':"extraordinary",
                    })
               new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
               res.append(new_training_record_line_obj) 
            elif linea.teaching:
                valRecLine.update({
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                res.append(new_training_record_line_obj)
                valRecLine.update({
                    'call':linea.call+1, 
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                res.append(new_training_record_line_obj)
            else:
                valRecLine.update({
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                res.append(new_training_record_line_obj )
        return res
                
    def action_wait(self, cr, uid, ids, *args):
        #######################################################################
        #OBJETOS#
        #######################################################################
        training_record_obj = self.pool.get('training.record')
        training_title_obj = self.pool.get('training.titles')
        training_session_obj = self.pool.get('training.session')
        training_seance_obj = self.pool.get('training.seance')
        training_record_line_obj = self.pool.get('training.record.line')
        sale_order_line_obj = self.pool.get('sale.order.line')
        #######################################################################
        for saleorder in self.browse(cr,uid,ids,*args):
            #TITULACION1 --Datos--
            cliente = saleorder.partner_id.id
            contacto = saleorder.contact_id.id
            edition = saleorder.session_id.id
            nombre_edicion = saleorder.session_id.name
            carrera = saleorder.session_id.offer_id.id
            titulo = saleorder.session_id.offer_id.name
            subscripcion = saleorder.subscription_id.id   
        #TITULACION 1 
        #mirar si exite expediente de ese alumno en esa carrear.
        existe_expediente = training_record_obj.search(cr,uid,[('student_id','=',contacto),('offer_id','=',carrera)]) 
        if not existe_expediente:
            #Coger titulo.
            id_titulo_existe = training_title_obj.search(cr,uid,[('name','=',titulo)])
            if not id_titulo_existe:
                raise osv.except_osv(_('ERROR'),_('Title must be a required field'))
            else:
                id_titulo = id_titulo_existe[0]
            #Crear Expediente y añadir edición.
            valExpediente={
                'subscription_id':subscripcion,
                'offer_id':carrera,
                'student_id':contacto,
                'title_id':id_titulo,
                'edition_ids':[(6,0,[edition])],
            }
            new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
            #Una vez creada la edicion recorrer las lineas del pedido ya añadirlas
            #a ese expediente.
            for saleorder in self.browse(cr,uid,ids,*args):
                list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                    if orderline.seance_id:
                        #funcion de crear lineas.
                        self._insert_data_on_record(cr, uid, ids, orderline,new_training_record_obj)
        else:
            #Mirar si exite edicion anterior de ese usuario para esa titulacion
            expediente_actual = training_record_obj.browse(cr,uid,existe_expediente[0])
            if edition not in expediente_actual.edition_ids:
#            existe_edicion_expediente = training_record_obj.search(cr,uid,[('edition_ids.id','=',edicion)])
#            if not existe_edicion_expediente:
                #Recoger ediciones existentes le añado el mio y hago el write.
                objEdicion = []
                if expediente_actual:
                    edition_list = expediente_actual.edition_ids
                    for exp_edition in edition_list:
                        objEdicion.append(exp_edition.id)
                    objEdicion.append(edition)
                    training_record_obj.write (cr,uid,existe_expediente[0],{'edition_ids':[(6,0,objEdicion)]})
                #INSERTAMOS SEANCES
                for saleorder in self.browse(cr,uid,ids,*args):
                    list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                    for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                        if orderline.seance_id:
                            #funcion de crear lineas.
                            self._insert_data_on_record(cr, uid, ids, orderline, existe_expediente[0])                         
        val = super(sale_order,self).action_wait(cr,uid,ids,*args)
        return val  
sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        #Función no se puede eredar, con lo cual la copiamos y la modificamos 
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.order_id.partner_invoice_id.id, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            valorDevolver = cur_obj.round(cr, uid, cur, taxes['total'])
            print valorDevolver
            if line.convalidate:
                if valorDevolver < 39:
                    valorDevolver = 39
                elif valorDevolver > 490:
                    valorDevolver = 490
            else:
                valorDevolver = valorDevolver
            res[line.id] = valorDevolver 
        return res
 
    _columns = {
        'seance_id':fields.many2one('training.seance', 'Seance'),
        'tipology': fields.related('seance_id','tipology',type='selection',selection=[
            ('basic', 'Basic'),
            ('mandatory', 'Mandatory'),
            ('optional', 'optional'),
            ('trunk', 'trunk'),
            ('degreework','Degree Work'),   
            ],string='Tipology',store=False),
#        'tipology': fields.selection([
#            ('basic', 'Basic'),
#            ('mandatory', 'Mandatory'),
#            ('optional', 'optional'),
#            ('trunk', 'trunk'),
#            ('degreework','Degree Work'),   
#            ], 'Tipology', required=True),
        'call': fields.integer('Call'),
        'teaching': fields.boolean('Teaching'),
        'convalidate': fields.boolean('Convalidate'),
        'matching': fields.boolean('Matching'),
        'coursenum_id' : fields.many2one('training.coursenum','Number Course'),
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal', digits_compute= dp.get_precision('Sale Price')),
    }
    
    
    def onchange_seance_id(self, cr, uid, ids, seance_id, session_id, contact, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        res = {}
        seance_obj = self.pool.get('training.seance')
        session_obj = self.pool.get('training.session')
        wizard_obj = self.pool.get('wiz.add.optional.fee')
        record_obj = self.pool.get('training.record')
        if seance_id:
            seance = seance_obj.browse(cr, uid, seance_id)
            session = session_obj.browse(cr, uid, session_id)
           
            record_id = record_obj.search(cr, uid, [('student_id', '=', contact), ('offer_id', '=', session.offer_id.id)])
            res = self.product_id_change(cr, uid, ids, pricelist, seance.course_id.product_id.id, qty, uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag)
            call = wizard_obj._find_call(cr, uid, seance, record_id[0])
            if not call:
                raise osv.except_osv(_('Error!'),_('This subject was passed!'))
            price = wizard_obj._get_subject_price(cr, uid, seance, session, call, teaching=False)
            res['value'].update({
                'tipology': seance.tipology,
                'product_uom_qty': seance.credits,
                'price_unit': price,
                'product_id': seance.course_id.product_id.id,
            })
        return res
    
sale_order_line()