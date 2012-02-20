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
        #######################################################
        for saleorder in self.browse(cr,uid,ids,*args):
            cliente = saleorder.partner_id.id
            edicion = saleorder.session_id.id
            carrera =saleorder.session_id.offer_id.id
            contacto = saleorder.contact_id.id
            titulo = saleorder.session_id.offer_id.name
            
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
        val = super(sale_order,self).action_wait(cr,uid,ids,*args)
        return val  
sale_order()