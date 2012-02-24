# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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

from osv import osv
from osv import fields
from tools.translate import _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

class training_create_session_seances(osv.osv_memory):

    _inherit = 'training.create.session.seances'
 
    _columns = {
            'avanzosc_date_from':fields.date('Star data', required=True, help="The start date of the planned session."),
            'avanzosc_date_to': fields.date('End data', required=True, help="The end date of the planned session."),
        }
    
    def next_step(self, cr, uid, ids, context=None):
        ''' Fills the create session wizard with the course lines of the offer '''
        if context is None:
            context = {}
        values = {}
        session_line_obj = self.pool.get('training.create.session.seances.line')
        for create_session in self.browse(cr, uid, ids, context = context):
            values['create_sessions_id'] = create_session.id
            data_from = create_session.avanzosc_date_from
            data_to = create_session.avanzosc_date_to
            for course in create_session.offer_id.course_ids:
                values['course_id'] = course.course_id.id
                values['avanzosc_date_from'] = data_from 
                values['avanzosc_date_to'] = data_to
                session_line_obj.create(cr, uid, values, context = context)
        return self.write(cr, uid, ids, {'state': 'second'}, context = context)
    
    def create_session(self, cr, uid, ids, context=None):
        """ 
        Create one session and the seances depending of the duration and the splitted time of the courses. 
        Ediciones --> training.session
        Sessiones --> training.seance
        
        search --> id
        browse --> object
        """
        ##################
        #Objetos
        #################################################################################################
        session_obj = self.pool.get('training.session')
        seance_obj = self.pool.get('training.seance')
        session_line_obj = self.pool.get('training.create.session.seances.line')
        tarinig_location = self.pool.get('training.location')
        training_offer_format = self.pool.get('training.offer.format')
        training_course_obj = self.pool.get('training.course')
        training_title_obj = self.pool.get('training.titles')
        training_credit_prices_seance_obj = self.pool.get('training.credit.prices.seance')
        #################################################################################################
        Obj=[]
        if context is None:
            context = {}
        values = {}
        #Fechas del sistema.
        hoy = datetime.now()
        year_actual = datetime.strftime(hoy,'%Y')
        next_year_ext = hoy + relativedelta(years=+1)
        next_year = datetime.strftime(next_year_ext,'%Y')
        #/Fechas
        #Obtención de datos pre-insert.
        ubicacion = tarinig_location.search(cr, uid, [])[0] or '/'
        formato = training_offer_format.search(cr,uid, [])[0] or '/'
        for create_session in self.browse(cr, uid, ids, context = context):
            fi =str(datetime.strptime(create_session.avanzosc_date_from,'%Y-%m-%d').year)
            ff =str(datetime.strptime(create_session.avanzosc_date_to,'%Y-%m-%d').year)
            nombre = create_session.offer_id.name+' ('+fi+'-'+ff+')'
            fecha_inicio = create_session.avanzosc_date_from
            fecha_fin = create_session.avanzosc_date_to
            curso = create_session.offer_id.id
            existe_edicion = session_obj.search(cr,uid,[('name','=',nombre)])
            if not existe_edicion:
                valEdiciones ={
                           'name':nombre,
                           'date_from':fecha_inicio,
                           'date_end':fecha_fin,
                           'date':fecha_fin,
                           'offer_id':curso,
                           'format_id':formato
                           }            
                new_session_obj = session_obj.create(cr,uid,valEdiciones,context=context)
                #Cogemos el precio del credito por combocatoria y la metemos en un objeto
                existe_titulo = training_title_obj.search(cr,uid,[('name','=',create_session.offer_id.name)])[0]
                for lineas in create_session.line_ids:
                    existe_curso = training_course_obj.search(cr,uid,[('name','=',lineas.course_id.name)])
                    coursenum = training_course_obj.browse(cr,uid,existe_curso[0]).coursenum_id.id
                    valSession = {
                                        'name':lineas.course_id.name+' ('+fi+'-'+ff+')',
                                        'date_from':fecha_inicio,
                                        'date_to':fecha_fin,
                                        'date':fecha_fin,
                                        'course_id':int(existe_curso[0]),
                                        'location_id':ubicacion,
                                        'coursenum_id':coursenum,
                                        'session_ids':[(6,0,[new_session_obj])],
                                 }
                    new_seance_obj = seance_obj.create(cr,uid,valSession,context=context)
                    
                existe_titulo = training_title_obj.search(cr,uid,[('name','=',create_session.offer_id.name)])[0]
                if existe_titulo:
                    for lin in training_title_obj.browse(cr,uid,existe_titulo).price_list:
                        val={
                                 'num_comb':lin.num_comb,
                                 'price_credit':lin.price_credit,
                                 'title_id':new_session_obj,
                            }
                        new_training_credit_prices_seance_obj=training_credit_prices_seance_obj.create(cr,uid,val)             
training_create_session_seances()


class training_create_session_seances_line(osv.osv_memory):
    _inherit = 'training.create.session.seances.line'
    _columns = {
            'avanzosc_date_from':fields.date('Star data', required=True, help="The start date of the planned session."),
            'avanzosc_date_to': fields.date('End data', required=True, help="The end date of the planned session."),
        }
training_create_session_seances_line()

class training_credit_prices_seance(osv.osv):
    _name='training.credit.prices.seance'
    _description='credit prices'
    _columns = {
            'num_comb': fields.char('Num.Combo',size=64),
            'price_credit': fields.float('Price per Credit'),
            
    }
training_credit_prices_seance()

class training_session(osv.osv):
    _inherit = 'training.session'
    _columns = {
                'price_list':fields.one2many('training.credit.prices.seance','title_id','Prices per Credit')
                }
training_session()

class training_credit_prices_seance(osv.osv):
    _inherit='training.credit.prices.seance'
    
    _columns = {
            'title_id': fields.many2one('training.session','Session'),
    }
training_credit_prices_seance()
