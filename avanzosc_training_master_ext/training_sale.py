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
    
    #Función que crea los Expedientes.
    def create_record(self, cr, uid, ids, contacto, carrera, titulo, edicion, nombre_edicion):
        #OBJETOS#
        #######################################################
        training_record_obj = self.pool.get('training.record')
        training_title_obj = self.pool.get('training.titles')
        training_session_obj = self.pool.get('training.session')
        training_seance_obj = self.pool.get('training.seance')
        training_record_line_obj = self.pool.get('training.record.line')
        #######################################################
        existe_expediente = training_record_obj.search(cr,uid,[('student_id','=',contacto),('offer_id','=',carrera)]) 
        if not existe_expediente:
            #titulo
            id_titulo = training_title_obj.search(cr,uid,[('name','=',titulo)])[0]
            #Crear Expediente y le linco la edicion
            valExpediente={
                           'offer_id':carrera,
                           'student_id':contacto,
                           'title_id':id_titulo,
                           'edition_ids':[(6,0,[edicion])],
                           }
            new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
            #Lincar seances nuevas.¿Como?
            #-Coger nombre edicion, y hacer un search
            #-con el ID de conseguido hacer un search en seances
            edicion_id = training_session_obj.search(cr,uid,[('name','=',nombre_edicion)])
            seances = training_seance_obj.search(cr, uid, edicion_id[0],[('coursenum_id.code','=',1)])
            for seance in seances:
                valRecLine={
                            'call':1,
                            'state':"--",
                            'submitted':"--",
                            'date':datetime.now(),
                            'session_id': seance.id,
                            'record_id':new_training_record_obj[0],  
                            }
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
            
        else:
            #mirar si exite edicion
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
                #Lincar seances.
                
    
    def action_wait(self, cr, uid, ids, *args):
        ####################
        #OBJETOS#
        #######################################################
        training_record_obj = self.pool.get('training.record')
        training_title_obj = self.pool.get('training.titles')
        training_session_obj = self.pool.get('training.session')
        training_seance_obj = self.pool.get('training.seance')
        training_record_line_obj = self.pool.get('training.record.line')
        #######################################################
        for saleorder in self.browse(cr,uid,ids,*args):
            cliente = saleorder.partner_id.id
            contacto = saleorder.contact_id.id
            #titulacion1
            edicion = saleorder.session_id.id
            nombre_edicion = saleorder.session_id.name
            carrera = saleorder.session_id.offer_id.id
            titulo = saleorder.session_id.offer_id.name
            #titulacion2
            edicion2 = saleorder.session_id2.id
            if edicion2:
                carrera2 = saleorder.session_id2.offer_id.id
                titulo2 = saleorder.session_id2.offer_id.name
            
        #TITULACION 1 --es obligatoria--
        #self.create_record(self, cr, uid, ids, contacto, carrera, titulo, edicion)
        existe_expediente = training_record_obj.search(cr,uid,[('student_id','=',contacto),('offer_id','=',carrera)]) 
        if not existe_expediente:
            #titulo
            id_titulo = training_title_obj.search(cr,uid,[('name','=',titulo)])[0]
            #Crear Expediente y le linco la edicion
            valExpediente={
                           'offer_id':carrera,
                           'student_id':contacto,
                           'title_id':id_titulo,
                           'edition_ids':[(6,0,[edicion])],
                           }
            new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
            #Lincar seances ¿como?
            edicion_id = training_session_obj.search(cr,uid,[('name','=',nombre_edicion)])
            seances_para_recorrer = training_seance_obj.search(cr, uid,[('coursenum_id.code','=',1),('session_ids','=',edicion_id[0])])
            for seance_id in seances_para_recorrer:
                seance = training_seance_obj.browse(cr,uid,seance_id)
                valRecLine={
                        'call':1,
                        'state':"nothing",
                        'submitted':"nothing",
                        'date':datetime.now(),
                        'name':seance.course_id.name,
                        'session_id': seance.id,
                        'record_id':new_training_record_obj,  
                        }
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
        else:
            #mirar si exite edicion
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
                #Lincar seances ¿como?
                
        #TITULACION 2 --es opcional--
        #self.create_record(self, cr, uid, ids, contacto, carrera2, titulo2, edicion2)
#            existe_expediente2 = training_record_obj.search(cr,uid,[('student_id','=',contacto),('offer_id','=',carrera2)])
#            if not existe_expediente:
#                #titulo
#                id_titulo2 = training_title_obj.search(cr,uid,[('name','=',titulo2)])[0]
#                #Crear Expediente y le linco la edicion
#                valExpediente={
#                           'offer_id':carrera2,
#                           'student_id':contacto,
#                           'title_id':id_titulo2,
#                           'edition_ids':[(6,0,[edicion2])],
#                           }
#                new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
#            else:
#            #mirar si exite edicion
#                existe_edicion_expediente = training_record_obj.search(cr,uid,[('edition_ids.id','=',edicion2)])
#                if not existe_edicion_expediente:
#                    #Recoger ediciones existentes le añado el mio y hago el write.
#                    objEdicion = []
#                    expediente_actual = training_record_obj.browse(cr,uid,existe_expediente[0])
#                    if expediente_actual:
#                        edition_list = expediente_actual.edition_ids
#                        for edition in edition_list:
#                            objEdicion.append(edition.id)
#                        objEdicion.append(edicion)
#                        training_record_obj.write (cr,uid,existe_expediente[0],{'edition_ids':[(6,0,objEdicion)]})
#                #Lincar seances ¿como? 
        val = super(sale_order,self).action_wait(cr,uid,ids,*args)
        return val  
sale_order()