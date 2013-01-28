# -*- encoding: utf-8 -*-
##############################################################################
#
#    AvanzOSC, Avanzed Open Source Consulting 
#    Copyright (C) 2011-2012 Iker Coranti (www.avanzosc.com). All Rights Reserved
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
#    along with this program.  If not__init__(), see http://www.gnu.org/licenses/.
#
##############################################################################
from osv import osv
from osv import fields

class res_partner_contact(osv.osv):

    _inherit = 'res.partner.contact'
    _description = 'res.partner.contact'
    
    def onchange_student(self, cr, uid, ids, student):
        #################################################################
        #OBJETOS
        #################################################################
        res_partner_contact_obj = self.pool.get('res.partner.contact')
        #################################################################
        
        contact = res_partner_contact_obj.browse(cr, uid, ids)
        value = {}
        if student:
            if (contact and not contact[0].student_number) or not contact:
                number=self.pool.get('ir.sequence').get(cr, uid, 'res.partner.contact')
                value.update({'student_number':number})
        return {'value':value}
    
         
#    def _stud_code(self, cr, uid, ids, name, args, context=None):
#        res = {}
#        code=''
#        res_partner_contact_obj = self.pool.get('res.partner.contact')
#        for contact in self.browse(cr, uid, ids, context=context):
#            type=contact.type
#            if type == 'student' :
#                print contact.registered
#                if contact.registered == False:
#                    res_partner_contact_obj.write(cr,uid,contact.id,{'registered':True})
#                    code=self.pool.get('ir.sequence').get(cr, uid, 'res.partner.contact')
#            res[contact.id]=code
#        return res
    
    _columns = {
            'student':fields.boolean('student'),
            'teacher':fields.boolean('teacher'),
            'other':fields.boolean('other'),
            'face':fields.boolean('Face'),
            'face_code':fields.char('Face Code', size=128),
            'online':fields.boolean('Online'),
            'online_code':fields.char('Online Code', size=128),
            'tutor':fields.many2one('res.partner.contact','Tutor'),
            #---------------- CAMPOS NUEVOS ------------
            'mailucav': fields.char('mailUcav',size=128),
            'swfile': fields.boolean('swFile'),
            'year_start_ucav': fields.integer('Start year UCAV'),
            'student_number':fields.char('Student Number', size=128),
            'identification_type': fields.many2one('training.identification.type','Identification type'),
            'birthplace': fields.many2one('training.city', 'Birth Place'),
            'birthstate':fields.many2one('res.country','Birth State'),
            'nationality': fields.char('Nationality', size=128),
            'residence_address': fields.char('Residence Address',size=128),
            'residence_city': fields.many2one('training.city','Residence city'),
            'residence_zip': fields.char('Zip', change_default=True, size=24),
            'telephone2': fields.char ('telephone2',size=64),
            'swalivef': fields.boolean('swAliveF'),
            'father_name':fields.char('Name',size=128),
            'father_studies':fields.many2one('training.parent.studies','Studies'),
            'father_profession':fields.many2one('training.workskills','Profession'),
            'swalivem': fields.boolean('swAliveM'),
            'mother_name':fields.char('Name',size=128),
            'mother_studies':fields.many2one('training.parent.studies','Studies'),
            'mother_profession':fields.many2one('training.workskills','Profession'),
            'type_access': fields.many2one('training.university.access.type','Access type'),
            'type_access_ucav': fields.many2one('training.ucav.access.type','Ucav access type'),
            'student_titulation': fields.char('Student titulation',size=128),
            'ref_secundary': fields.selection([('0','Do not know'),
                                               ('1','Bachiller'),
                                               ('2','FP')],'Ref_Secundary'),
            #'tree_option': fields.many2one('','Tree option'),
            'distrito': fields.char('distrito',size=128),
            'selectivity_call': fields.integer('Selectivity call'),
            'selectivity_mark': fields.float('Selectivity mark'),
            'start_year':fields.integer('Start year'),
            'work':fields.many2one('training.workskills','Work'),
            'swleft': fields.boolean('swLeft'),
            'left_reason': fields.many2one('training.left.reason','Left reason'),
            'swresguardo': fields.boolean('swResguardo'),
            'uniresguardo': fields.many2one('training.universities','uniresguardo'),
            'swtraslado': fields.boolean('swTraslado'),
            'date_traslado':fields.date('Date Traslado'),
            'swresguardo2': fields.boolean('swResguardo2'),
            'uniresguardo2': fields.many2one('training.universities','uniresguardo2'),
            'swtraslado2': fields.boolean('swTraslado2'),
            'date_traslado2':fields.date('Date Traslado 2'),
            'idunidest':fields.many2one('training.universities','Uni.Dest.'),
            'large_family': fields.boolean('Large family'),
            'type_large_family': fields.selection([('1','General'),
                                                   ('2','Special'),
                                                   ('3','Other')],'Type large family'),
            'centroensmedia': fields.char('Centro Enseñanza Media',size=128),
            'naturalezaensmedia': fields.selection([('1','Private'),
                                                    ('2','Public'),
                                                    ('3','Public Private')],'Naturaleza'),
            'cityensmedia': fields.many2one('training.city','City Ens.Media'),
            'countryensmedia': fields.many2one('res.country','Country Ens.Media'),
            #'stateensmedia': fields.many2one('','State Ens.Media'),
            'especialidadingresouni':fields.many2one('training.specialities','Especialidad Ingreso'),
            'authorized_person_ids':fields.one2many('authorized.person', 'contact_id', "Authorized People"),
            #---------- /CAMPOS NUEVOS ----------
        }
    _defaults = {
#                'student_code': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'res.partner.contact'),
#                'type':lambda *a: 'student',
#                'student':lambda *a:'True',
                 }
res_partner_contact()
