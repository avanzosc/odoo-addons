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
import decimal_precision as dp

class training_create_session_seances(osv.osv_memory):

    _inherit = 'training.create.session.seances'
 
    _columns = {
            'avanzosc_date_from' : fields.datetime('First semester start', required=True, help="The data when course begins"),
            'avanzosc_date_to': fields.datetime('First semester end', required=True, help = "The first semester end date of the planned session"),
            'semester': fields.selection([('first_semester','First Semester'),('second_semester','Second Semester')],'Semester',required=True),
            'calendar':fields.many2one('training.course.calendar','Calendar',required=True,help = "Select the academic year."),
        }
    
    def next_step(self, cr, uid, ids, context=None):
        ''' Fills the create session wizard with the course lines of the offer '''
        #OBJETOS
        ##############################################################
        session_line_obj = self.pool.get('training.create.session.seances.line')
        training_course_calendar_obj = self.pool.get('training.course.calendar')
        ##############################################################
        if context is None:
            context = {}
        values = {}
        
        for create_session in self.browse(cr, uid, ids, context = context):
            values['create_sessions_id'] = create_session.id
            calendar_id =create_session.calendar.id
            
            for calendar in training_course_calendar_obj.browse(cr,uid,[calendar_id]):
                start_semester1 = calendar.first_semester_start
                end_semester1 = calendar.first_semester_end
                start_semester2 = calendar.second_semester_start
                end_semestre2 = calendar.second_semester_end
                
            for course in create_session.offer_id.course_ids:
                semester = course.course_id.semester
                if semester == 'first_semester':
                    data_from = start_semester1
                    data_to = end_semester1
                if semester == 'second_semester':
                    data_from = start_semester2
                    data_to = end_semestre2
                
                values['course_id'] = course.course_id.id
                values['semester'] = course.course_id.semester
                values['avanzosc_date_from'] = data_from 
                values['avanzosc_date_to'] = data_to
                values['tipology'] = course.tipology
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
        training_course_calendar_obj = self.pool.get('training.course.calendar')
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
            #Año
            #-------------------------------------------------------
            fi =str(datetime.strptime(create_session.calendar.first_semester_start,'%Y-%m-%d %H:%M:%S').year)
            ff =str(datetime.strptime(create_session.calendar.second_semester_end,'%Y-%m-%d %H:%M:%S').year)
            #-------------------------------------------------------
            nombre = create_session.offer_id.name+' ('+fi+'-'+ff+')'
            #fecha_inicio = create_session.avanzosc_date_from
            #fecha_fin = create_session.avanzosc_date_to
            curso = create_session.offer_id.id
            existe_edicion = session_obj.search(cr,uid,[('name','=',nombre)])
            if not existe_edicion:
                valEdiciones ={
                           'name':nombre,
                           'date_from':create_session.calendar.first_semester_start,
                           'date_end':create_session.calendar.second_semester_end,
                           'date':hoy,
                           'offer_id':curso,
                           'format_id':formato
                           }            
                new_session_obj = session_obj.create(cr,uid,valEdiciones,context=context)
                #Cogemos el precio del credito por combocatoria y la metemos en un objeto
                existe_titulo = training_title_obj.search(cr,uid,[('name','=',create_session.offer_id.name)])[0]
                for lineas in create_session.line_ids:
                    existe_curso = training_course_obj.search(cr,uid,[('name','=',lineas.course_id.name)])
                    coursenum = training_course_obj.browse(cr,uid,existe_curso[0]).coursenum_id.id
                    creditos =  training_course_obj.browse(cr,uid,existe_curso[0]).credits
                    id_titulo = training_title_obj.search(cr,uid,[('name','=',create_session.offer_id.name)])[0]
                    titulo = training_title_obj.browse(cr, uid, id_titulo).id
                    valSeance = {
                                        'name':lineas.course_id.name+' ('+fi+'-'+ff+')',
                                        'date_from':lineas.avanzosc_date_from,
                                        'date_to':lineas.avanzosc_date_to,
                                        'date':hoy,
                                        'semester': lineas.semester,
                                        'course_id':int(existe_curso[0]),
                                        'location_id':ubicacion,
                                        'coursenum_id':coursenum,
                                        'credits':creditos,
                                        'title_id': titulo,
                                        'tipology':lineas.tipology,
                                        'duration':1,
                                        'session_ids':[(6,0,[new_session_obj])],
                                 }
                    new_seance_obj = seance_obj.create(cr,uid,valSeance,context=context)
                    
                existe_titulo = training_title_obj.search(cr,uid,[('name','=',create_session.offer_id.name)])[0]
                if existe_titulo:
                    for lin in training_title_obj.browse(cr,uid,existe_titulo).price_list:
                        val={
                                 'num_comb':lin.num_comb,
                                 'price_credit':lin.price_credit,
                                 'price_credit_teaching': lin.price_credit_teaching,
                                 'title_id':new_session_obj,
                            }
                        new_training_credit_prices_seance_obj=training_credit_prices_seance_obj.create(cr,uid,val)             
training_create_session_seances()


class training_create_session_seances_line(osv.osv_memory):
    _inherit = 'training.create.session.seances.line'
    _columns = {
            'avanzosc_date_from':fields.date('Star data', required=True, help="The start date of the planned session."),
            'avanzosc_date_to': fields.date('End data', required=True, help="The end date of the planned session."),
            'semester': fields.selection([('first_semester','First Semester'),('second_semester','Second Semester')],'Semester',required=True),
            'tipology': fields.selection([
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('trunk','Trunk'),
                ('degreework', 'Degree work'),
        ], 'Tipology',required=True),
        }
training_create_session_seances_line()

class training_credit_prices_seance(osv.osv):
    _name='training.credit.prices.seance'
    _description='credit prices'
    _columns = {
            'num_comb': fields.integer('Num.Combo',size=64),
            'price_credit': fields.float('Price per Credit', digits_compute=dp.get_precision('Account')),
            'price_credit_teaching': fields.float('Price per Credit (Teaching)', digits_compute=dp.get_precision('Account')),
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
