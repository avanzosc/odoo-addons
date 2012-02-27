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


class sale_order(osv.osv):
    _inherit = "sale.order"
    
    _columns = {
        'contact_id': fields.many2one('res.partner.contact', 'Contact', required=True),
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

    def action_wait(self, cr, uid, ids, *args):
        ####################
        #OBJETOS#
        #######################################################
        training_record_obj = self.pool.get('training.record')
        training_title_obj = self.pool.get('training.titles')
        training_session_obj = self.pool.get('training.session')
        training_seance_obj = self.pool.get('training.seance')
        training_record_line_obj = self.pool.get('training.record.line')
        sale_order_line_obj = self.pool.get('sale.order.line')
        #######################################################
        for saleorder in self.browse(cr,uid,ids,*args):
            #TITULACION1 --Datos--
            cliente = saleorder.partner_id.id
            contacto = saleorder.contact_id.id
            edicion = saleorder.session_id.id
            nombre_edicion = saleorder.session_id.name
            carrera = saleorder.session_id.offer_id.id
            titulo = saleorder.session_id.offer_id.name    
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
                           'offer_id':carrera,
                           'student_id':contacto,
                           'title_id':id_titulo,
                           'edition_ids':[(6,0,[edicion])],
                           }
            new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
            #Una vez creada la edicion recorrer las lineas del pedido ya añadirlas
            #a ese expediente.
            for saleorder in self.browse(cr,uid,ids,*args):
                list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                    #my_seance_id = training_seance_obj.search(cr,uid,[('course_id.product_id','=',orderline.product_id.id),('session_ids','=',edicion)])
                    if orderline.seance_id:
                        valRecLine={
                                    'call':orderline.call,
                                    'state':"nothing",
                                    'submitted':"nothing",
                                    'date':datetime.now(),
                                    'name':orderline.product_id.name,
                                    'session_id': orderline.seance_id.id,
                                    'record_id':new_training_record_obj,  
                                    }
                        new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
        else:
            #Mirar si exite edicion anteriro de ese usuario para esa titulacion
            existe_edicion_expediente = training_record_obj.search(cr,uid,[('edition_ids.id','=',edicion)])
            if not existe_edicion_expediente:
                #Recoger ediciones existentes le añado el mio y hago el write.
                objEdicion = []
                expediente_actual = training_record_obj.browse(cr,uid,existe_expediente[0])
                if expediente_actual:
                    edition_list = expediente_actual.edition_ids
                    for edition in edition_list:
                        objEdicion.append(edition.id)
                    objEdicion.append(edicion)
                    training_record_obj.write (cr,uid,existe_expediente[0],{'edition_ids':[(6,0,objEdicion)]})
                #INSERTAMOS SEANCES
                for saleorder in self.browse(cr,uid,ids,*args):
                    list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                    for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                        if orderline.seance_id:
                            valRecLine={
                                    'call':orderline.call,
                                    'state':"nothing",
                                    'submitted':"nothing",
                                    'date':datetime.now(),
                                    'name':orderline.product_id.name,
                                    'session_id': orderline.seance_id.id,
                                    'record_id':existe_expediente[0],  
                                    }
                            new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                    
        val = super(sale_order,self).action_wait(cr,uid,ids,*args)
        return val  
sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
 
    _columns = {
            'seance_id':fields.many2one('training.seance', 'Seance'),
        }
sale_order_line()