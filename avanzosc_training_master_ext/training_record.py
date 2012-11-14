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

from datetime import datetime,timedelta
from osv import osv
from osv import fields
from tools.translate import _

class training_record(osv.osv):
    _name = 'training.record'
    _description = 'Training Record'
training_record()

class training_record_line(osv.osv):
    _name = 'training.record.line'
    _description = 'Training Record Line' 
training_record_line()

class validate_date(osv.osv):
    _name = 'validate.date'
    _description = 'Validate date' 
validate_date()

class validate_date_line(osv.osv):
    _name='validate.date.line'
    _description='Validate Date Line'
    _columns = {
                'name': fields.char('Name', size=64),
                'date': fields.date('Date'),
                'validate_date_id': fields.many2one('validate.date','Session'),
                'record_line_ids': fields.one2many('training.record.line', 'validate_date_line_id', 'Record Lines'),
                }
validate_date_line()

class validate_date(osv.osv):
    _inherit='validate.date'
    _columns = {
                'name': fields.char('Session', size=64),
                'validate_date_line_ids': fields.one2many('validate.date.line', 'validate_date_id', 'Validate Date Lines'),
                }
validate_date()

class training_record_line(osv.osv):
     _inherit = 'training.record.line'
     
#     def _seance_course_name(self, cr, uid, ids, name, args, context=None):
#        res = {}
#        for record_line in self.browse(cr, uid, ids, context=context):
#            if record_line.seance_id.name:
#                seance_course=record_line.seance_id.course_id.name
#            else:
#                seance_course=record_line.external_course_id.name
#            res[record_line.id]=seance_course
#        return res
 
     _columns = {
         'name': fields.char('Seance Name', size=128,states={'closed': [('readonly', True)]}),
         'seance_id': fields.many2one('training.seance', 'Seance',readonly=True, states={'closed': [('readonly', True)]}),
         'university':fields.many2one('training.universities', 'Universities',states={'closed': [('readonly', True)]}),
         'session':fields.char('Session', size=64),
         'validation_type':fields.selection([('internal', 'Internal'), ('external', 'External')], 'Validation Type'),
         'internal_course_id':fields.many2one('training.seance','Internal course'),
         'external_course_id':fields.many2one('training.external.course','External course'),
#         'seance_course_name':fields.function(_seance_course_name,type='char',method=True, string='Seance Name',readonly=True),
         'course_code':fields.char('Course Code', size=64,states={'closed': [('readonly', True)]}),
         'validate_date_line_id': fields.many2one('validate.date.line','Validate date',states={'closed': [('readonly', True)]}),
         'cycle':fields.selection([('cycle1', 'Cycle 1'), ('cycle2', 'Cycle 2')], 'Cycle'),
         'pass_date':fields.date('Pass Date',states={'closed': [('readonly', True)]}),
         'notes':fields.text('Notes'),
         'date': fields.date('Date',states={'closed': [('readonly', True)]}),
         'year': fields.integer('Year'),
         'credits': fields.integer('Credits', required=True, help="Course credits" ,states={'closed': [('readonly', True)]}),
         'tipology': fields.selection([
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('freechoice','Free Choice'),
#                ('trunk', 'Trunk'),
                ('complement','Training Complement'),
                ('replacement','Replacement'),
                ('degreework','Degree Work'),   
          ],'Tipology', required=True, states={'closed': [('readonly', True)]}),
         'call': fields.integer('Call', states={'closed': [('readonly', True)]}),
         'mark': fields.float('Mark', states={'closed': [('readonly', True)]}),
         'state': fields.selection([
             ('not_sub', 'Not Submitted'),
             ('noassistance','No Assistance'),
             ('failed', 'Failed'),
             ('passed', 'Passed'),
             ('merit', 'Merit'),
             ('distinction', 'Distinction'),
             ('special distinction', 'Special Distinction'),
             ('compensation', 'Approved by Compensation'),
             ('no_schooling','No Schooling'),
         ],'State', required=True),
         'type': fields.selection([
             ('ordinary','Ordinary'),
             ('extraordinary','Extraordinary'),
             ('validated','Validated'),
             ('recognized','Recognized'),
             ('adapted','Adapted'),
         ],'Type', required=True, states={'closed': [('readonly', True)]}),
         'record_id': fields.many2one('training.record', 'Record', required=True, states={'closed': [('readonly', True)]}),
         'coursenum_id' : fields.many2one('training.coursenum','Number Course', states={'closed': [('readonly', True)]}),
         'checkrec': fields.boolean('CheckRec', states={'closed': [('readonly', True)]}),
         'clear': fields.boolean('Clear', states={'closed': [('readonly', True)]}),
         'student_id': fields.related('record_id','student_id', type="many2one", relation="res.partner.contact", string="Student",readonly=True, store=True),
         'student_doc': fields.related('student_id','identification_doc', type="char",size=64, string="Student ID"),         
         'offer_id': fields.related('record_id','offer_id', type="many2one",relation="training.offer", string="Offer", store=True),         
         #RELATED('id_tabla', 'id_campo_a_mostrar',type, relation, string,store)    
     }

     _defaults = {
         'state': lambda *a: 'not_sub',
         'type': lambda *a: 'validated',
         'tipology': lambda *a: 'basic',
         'validation_type': lambda *a: 'internal',
         
     }

     def onchange_mark(self, cr, uid, ids, mark,state, context=None):
         '''
         Un onchange para que las notas se cambien dependindo de la nota
         numérica introducida
         '''
         res = {}
         if mark == -1:
             res = {
                 'state': 'noassistance',
             }
         elif mark < 5:
             res = {
                 'state': 'failed',
             }
         elif mark < 7:
             res = {
                 'state': 'passed',
             }
         elif mark < 9:
             res = {
                 'state': 'merit',
             }
         elif mark <=10:
            res = {
                 'state': 'distinction',
             }
         else: 
            raise osv.except_osv(_('Error!'),_('Mark can not be higher than 10'))
         return {'value': res}
     
     def onchange_external_course(self, cr, uid, ids, course_id, context=None):
         '''
         Onchange para que cuando elijamos el curso se rellenen automaticamente los 
         demas campos. Con los cursos internos de la propia universidad
         '''
         res = {}
         if course_id == False:
            return {'value': res}
         else:
            res = {}
            external_course_obj = self.pool.get ('training.external.course')
            for course in external_course_obj.browse(cr, uid, [course_id]):
                res = {
                    'course_code': course.course_code,
                    'name':course.name,
                    'university': course.university.id,
                    'credits':course.credits,
                    }
            return {'value': res}
        
     def onchange_internal_course(self, cr, uid, ids, course_id, context=None):
         '''
         Onchange para que cuando elijamos el curso se rellenen automaticamente los 
         demas campos. Con los cursos externos de la propia universidad
         '''
         res = {}
         if course_id == False:
            return {'value': res}
         else:
            res = {}
            external_course_obj = self.pool.get ('training.seance')
            for seance in external_course_obj.browse(cr, uid, [course_id]):
                a=seance.name
                a=a.split('(')
                a=a[1]
                a=a.split(')')
                a=a[0]
                session=a[2]+a[3]+'-'+a[7]+a[8]
                res = {
                    'course_code': seance.course_id.course_code,
                    'name':seance.course_id.name,
                    'university': 1,
                    'credits':seance.course_id.credits,
                    'cycle':seance.course_id.cycle,
                    'session':session,
                    'mark':6.0,
                    'state':"passed"
                    }
            return {'value': res}
        
     def onchange_validate_date(self, cr, uid, ids, validate_date_line_id, context=None):
         '''
         Onchange para 
         '''
         res = {}
         if validate_date_line_id == False:
            return {'value': res}
         else:
            res = {}
            validate_date_obj = self.pool.get ('validate.date.line')
            for validate_date_line in validate_date_obj.browse(cr, uid, [validate_date_line_id]):
                res = {
                    'session':validate_date_line.validate_date_id.name,
                    }
            return {'value': res}
        
training_record_line()

class training_record_second_cycle_access(osv.osv):
    '''
    Se crea una nueva pestaña en la cual se hace un plan
    personalizado para esa persona que posteriormente se lleva al pedido de venta.
    '''
    #Iker 19/10/2012
    _name ='training.record.second.cycle.access'
    _description = 'Second cycle access plan on training record object'
    
    _columns={
         'course_id': fields.many2one('training.course', 'Course', states={'closed': [('readonly', True)]}),
         'course_code':fields.char('Course Code', size=64,states={'closed': [('readonly', True)]}),
         'cycle':fields.selection([('cycle1', 'Cycle 1'), ('cycle2', 'Cycle 2')], 'Cycle'),
         'credits': fields.integer('Credits', required=True, help="Course credits" ,states={'closed': [('readonly', True)]}),
         'sustitutive': fields.selection([
                                          ('yes','YES'),
                                          ('no','NO'),
                                          ],'Sustitutive',required=True,states={'closed': [('readonly', True)]}),
         'state': fields.selection([
                                    ('approved','Approved'),
                                    ('*','*'),
                                    ],'State',required=True,states={'closed': [('readonly', True)]}),
         'tipology': fields.selection([
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('freechoice','Free Choice'),
#                ('trunk', 'Trunk'),
                ('complement','Training Complement'),
                ('replacement','Replacement'),
                ('degreework','Degree Work'),   
          ],'Tipology', required=True, states={'closed': [('readonly', True)]}),
         'type': fields.selection([
             ('ordinary','Ordinary'),
             ('extraordinary','Extraordinary'),
             ('validated','Validated'),
             ('recognized','Recognized'),
             ('adapted','Adapted'),
         ],'Type', required=True, states={'closed': [('readonly', True)]}),
         'record_id': fields.many2one('training.record', 'Record', required=True, states={'closed': [('readonly', True)]}),
         'coursenum_id' : fields.many2one('training.coursenum','Number Course', states={'closed': [('readonly', True)]}),
         'clear': fields.boolean('Clear', states={'closed': [('readonly', True)]}),
         'student_id': fields.related('record_id','student_id', type="many2one", relation="res.partner.contact", string="Student",readonly=True, store=True),
         'student_doc': fields.related('student_id','identification_doc', type="char",size=64, string="Student ID"),         
         'offer_id': fields.related('record_id','offer_id', type="many2one",relation="training.offer", string="Offer", store=True),         
         #RELATED('id_tabla', 'id_campo_a_mostrar',type, relation, string,store)    
     }
    _defaults = {
         'cycle': lambda *a:'cycle2',
         'state': lambda *a: 'not_sub',
         'type': lambda *a: 'validated',
         'tipology': lambda *a: 'basic',
         #'validation_type': lambda *a: 'internal',
       }  
    
    def onchange_course(self, cr, uid, ids, course_id, context=None):
        ###########################################################
        # OBJETOS
        ###########################################################
        training_course_obj = self.pool.get("training.course")
        ###########################################################
        res = {}
        if course_id == False:
            return {'value': res}
        else:
             for tt in training_course_obj.browse(cr, uid, [course_id]):
                  res = {
                    'credits': tt.credits or 0,
                    'course_code': tt.course_code or 'Error',
                    }
        return {'value': res}
             
        
training_record_second_cycle_access()

class training_record_credits_line(osv.osv):
     #XABI 14/09/2012
     _name = 'training.record.credits.line'
     _description = 'Training Record Session Credits'
     
     def _calculate_session_credits(self, cr, uid, ids, field_name, arg, context={}):                                                
        '''   
         Calculos de los creditos(creditos de matricula y convalidados) aprobados,suspendidos y no presentados por Curso 
        '''
        ##################################################################
        training_record_obj = self.pool.get('training.record')
        training_record_line_obj = self.pool.get('training.record.line')
        training_record_credits_line_obj=self.pool.get('training.record.credits.line')
        ###################################################################
        res = {}
        for session_credit_line in self.browse(cr, uid, ids):
            credits=0
            val_credits=0
            passed_credits=0
            passed_percent=0
            not_passed_credits=0
            not_passed_percent=0
            no_assistance_credits=0
            no_assistance_percent=0
            mark=0
            res[session_credit_line.id] = {
                'credits': 0,
                'val_credits': 0,
                'passed_credits': 0,
                'passed_percent': 0,
                'not_passed_credits': 0,
                'not_passed_percent': 0,
                'no_assistance_credits': 0,
                'no_assistance_percent': 0,
                'avg_mark':0
            }
            record_object=training_record_obj.browse(cr, uid, session_credit_line.record_id.id)
            seance_ids=[]
            passed_ids=[]
            failed_ids=[]
            no_assistance_ids=[]
            val_seance_ids=[]
            for record_line in record_object.record_line_ids:
                if record_line.session == session_credit_line.session:
                    if record_line.type in ('ordinary','extraordinary'):
                        seance=record_line.seance_id.id
                        if seance not in seance_ids:
                            seance_ids.append(seance)
                            credits+=record_line.credits
                        if record_line.state in ('passed','merit','distinction'):
                            if seance not in passed_ids:
                                passed_ids.append(seance)
                                passed_credits+=record_line.credits
                            if seance in failed_ids:
                                not_passed_credits-=record_line.credits
                            if seance in no_assistance_ids:
                                no_assistance_credits-=record_line.credits
                            if record_line.type == 'ordinary':
                                mark+=record_line.mark*record_line.credits
                            else:
                                mark+=record_line.mark*record_line.credits
                                for rec_line in record_object.record_line_ids:
                                    if rec_line.seance_id.id==seance and rec_line.call < record_line.call :
                                        if rec_line.state in ('failed','passed','merit','distinction'):
                                            mark-=rec_line.mark*rec_line.credits
                        elif record_line.state == 'failed':
                            if seance not in failed_ids and seance not in passed_ids:
                                failed_ids.append(seance)
                                not_passed_credits+=record_line.credits
                            if seance in no_assistance_ids:
                                no_assistance_credits-=record_line.credits
                            if record_line.type == 'ordinary':
                                mark+=record_line.mark*record_line.credits
                            else:
                                mark+=record_line.mark*record_line.credits
                                for rec_line in record_object.record_line_ids:
                                    if rec_line.seance_id.id==seance and rec_line.call < record_line.call:
                                        if rec_line.state == 'failed':
                                            mark-=rec_line.mark*rec_line.credits
                        elif record_line.state == 'noassistance':
                            if seance not in no_assistance_ids and seance not in failed_ids and seance not in passed_ids:
                                no_assistance_credits+=record_line.credits
                                no_assistance_ids.append(seance)
                    else:
                        seance=record_line.external_course_id.id
                        if seance not in val_seance_ids:
                           val_seance_ids.append(seance)
                           val_credits+=record_line.credits
            if credits == 0:
                mark=0
                passed_percent=0
                not_passed_percent=0
                no_assistance_percent=0
            else:
                mark=round((mark/credits),2)
                passed_percent=round(((float(passed_credits)*100)/credits),2)
                not_passed_percent=round(((float(not_passed_credits)*100)/credits),2)
                no_assistance_percent=round(((float(no_assistance_credits)*100)/credits),2)
            res[session_credit_line.id]['credits'] = credits
            res[session_credit_line.id]['val_credits'] = val_credits
            res[session_credit_line.id]['passed_credits'] = passed_credits
            res[session_credit_line.id]['passed_percent'] = passed_percent
            res[session_credit_line.id]['not_passed_credits'] = not_passed_credits
            res[session_credit_line.id]['not_passed_percent'] = not_passed_percent
            res[session_credit_line.id]['no_assistance_credits'] = no_assistance_credits
            res[session_credit_line.id]['no_assistance_percent'] = no_assistance_percent
            res[session_credit_line.id]['avg_mark'] = mark     
        return res
     
     _columns = {
         'record_id': fields.many2one('training.record','Record'),
         'session':fields.char('Session',size=32,readonly=True),
         'credits': fields.function(_calculate_session_credits, method=True, type='float',string='Credits', multi='sum'),
         'val_credits': fields.function(_calculate_session_credits, method=True, type='float', string='Validated Credits', multi='sum'),
         'passed_credits': fields.function(_calculate_session_credits, method=True, type='float', string='Passed Credits', multi='sum'),
         'passed_percent': fields.function(_calculate_session_credits, method=True, type='float', string='Passed %', multi='sum'),
         'not_passed_credits': fields.function(_calculate_session_credits, method=True, type='float', string='Not Passed Credits', multi='sum'),
         'not_passed_percent': fields.function(_calculate_session_credits, method=True, type='float', string='Not Passed %', multi='sum'),
         'no_assistance_credits': fields.function(_calculate_session_credits, method=True, type='float', string='No Assistance Credits', multi='sum'),
         'no_assistance_percent': fields.function(_calculate_session_credits, method=True, type='float', string='No Assistance %', multi='sum'),
         'avg_mark':fields.function(_calculate_session_credits, method=True, type='float', string='Session mark', multi='sum'),
    }
     
training_record_credits_line()

class training_record(osv.osv):
    #Urtzi
    #Iker--08/05/2012
    #Xabi 18/09/2012
    _inherit = 'training.record'
    def _calculate_credits(self, cr, uid, ids, field_name, arg, context={}):
        '''   
         Calculos de los creditos aprobados divididos por categorias: Trunk,
         Mandatory, Optional, Basic 
        '''
        
        res = {}
        for record in self.browse(cr, uid, ids):
            sum_total = 0
            res[record.id] = {
                'curr_basic1': 0,
                'curr_mandatory1': 0,
                'curr_optional1': 0,
                'curr_freechoice1': 0,
                'curr_basic2': 0,
                'curr_mandatory2': 0,
                'curr_optional2': 0,
                'curr_freechoice2': 0,
                'curr_degree': 0,
                'curr_total': 0,
                'curr_complement':0,
                'curr_replacement':0,
                'total_cycle': 0,
                'progress_rate': 0,
            }
            
            sum_total += record.basic_cycle1
            sum_total += record.mandatory_cycle1
            sum_total += record.optional_cycle1
            sum_total += record.freechoice_cycle1
            sum_total += record.basic_cycle2
            sum_total += record.mandatory_cycle2
            sum_total += record.optional_cycle2
            sum_total += record.freechoice_cycle2
            sum_total += record.degree_cycle
            sum_total += record.complement_credits
            sum_total += record.replacement_credits
            res[record.id]['total_cycle'] = sum_total
            
            sum_basic1 = 0
            sum_mandatory1 = 0
            sum_optional1 = 0
            sum_freechoice1 = 0
            sum_basic2 = 0
            sum_mandatory2 = 0
            sum_optional2 = 0
            sum_freechoice2 = 0
            sum_degree = 0
            sum_complement= 0
            sum_replacement= 0
            sum_curr = 0
            
            for line in record.record_line_ids:
                if line.state in ('passed','merit','distinction'):
                    if line.tipology == 'basic':
                        if line.cycle== 1:
                            sum_basic1 += line.credits
                        else:
                            sum_basic1 += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'mandatory':
                        if line.cycle== 1:
                            sum_mandatory1 += line.credits
                        else:
                            sum_mandatory2 += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'optional':
                        if line.cycle== 1:
                            sum_optional1 += line.credits
                        else:
                            sum_optional2 += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'freechoice':
                        if line.cycle== 1:
                            sum_freechoice1 += line.credits
                        else:
                            sum_freechoice2 += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'degreework':
                        sum_degree += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'complement':
                        sum_complement += line.credits
                        sum_curr = line.credits
                    elif line.tipology == 'replacement':
                        sum_replacement += line.credits
                        sum_curr = line.credits
            res[record.id]['curr_basic1'] = sum_basic1
            res[record.id]['curr_mandatory1'] = sum_mandatory1
            res[record.id]['curr_optional1'] = sum_optional1
            res[record.id]['curr_freechoice1'] = sum_freechoice1
            res[record.id]['curr_basic2'] = sum_basic2
            res[record.id]['curr_mandatory2'] = sum_mandatory2
            res[record.id]['curr_optional2'] = sum_optional2
            res[record.id]['curr_freechoice2'] = sum_freechoice2
            res[record.id]['curr_degree'] = sum_degree
            res[record.id]['curr_complement'] = sum_complement
            res[record.id]['curr_replacement'] = sum_replacement
            res[record.id]['curr_total'] = sum_curr
        return res
    
    def _record_rate(self, cr, uid, ids, field_name, arg, context={}):
        '''   
         Calculos de la barra de progreso de aprobados.  
        '''
        res = {}
        for record in self.browse(cr, uid, ids):
            res[record.id]={
                            'progress_rate': 0,
                            'progress_rate_ing': 0,
                            }
            if record.curr_total > 0 and record.total_cycle > 0:
                res[record.id]['progress_rate'] = (float(record.curr_total) * 100) / float(record.total_cycle)
                res[record.id]['progress_rate_ing'] = round((float(record.curr_total-record.curr_degree) * 100) / float(record.total_cycle-record.degree_cycle),2)
            else:
                res[record.id] = 0
        return res
    
    def _average_mark_calc(self, cr, uid, ids, name, arg, context={}):
        
        ##########################################################
        # Xabi 25/09/2012
        '''
        Calcula la nota media 
        '''
        
        ##########################################################
        # OBJETOS
        ##########################################################
        record_obj = self.pool.get ('training.record')
        record_line_obj = self.pool.get('training.record.line')
        ##########################################################
        # ARRAYS
        ##########################################################
        res={}
        ##########################################################
        add_credits = 0.0
        add_lectures = 0.0
        average_mark = 0.0
        mark = 0.0
        for record in self.browse(cr,uid,ids):
            record_line = record_line_obj.search(cr, uid,[('record_id','=',record.id)])
            for lines in record_line_obj.browse(cr, uid, record_line, context=None):
                if lines:
                    if lines.state in ('passed','merit','distinction'):
                        add_credits += lines.credits
                        mark+=lines.mark*lines.credits
            if add_credits > 0.0:
                average_mark = round((mark/add_credits),2)
            else:
                 average_mark = 0.0 
            res[record.id] = average_mark
        return res
    
    def _calculate_universities(self, cr, uid, ids, name, arg, context={}):
        
        #XABI 14/09/2012
        
        '''   
         Calculo de las universidades del expediente.  
        '''
        ##########################################################
        # OBJETOS
        ##########################################################
        record_obj = self.pool.get ('training.record')
        record_line_obj = self.pool.get('training.record.line')
        
        res={}
        for record in self.browse(cr,uid,ids):
            record_line = record_line_obj.search(cr, uid,[('record_id','=',record.id)])
            univ_ids=[]
            for lines in record_line_obj.browse(cr, uid, record_line, context=None):
                if lines:
                    if lines.university:
                        if lines.university.id not in univ_ids:
                            univ_ids.append(lines.university.id)
            if univ_ids:
                univ_ids.sort()
            res[record.id] = univ_ids
        return res
 
    _columns = {
        'name':fields.char('Record Nº', size=64, required=True, states={'closed': [('readonly', True)]}),
        'graduate_data':fields.date('Graduate data'),
        'issecondcycle': fields.boolean('2nd Cycle Plan'),
        'access_second_plan':fields.one2many('training.record.second.cycle.access','record_id',states={'closed': [('readonly', True)]}),
        'student_id': fields.many2one('res.partner.contact', 'Student',required=True, states={'closed': [('readonly', True)]} ),
        'offer_id': fields.many2one('training.offer', 'Offer', required=True, states={'closed': [('readonly', True)]}),
        'edition_ids': fields.many2many('training.session','training_record_edition_rel','edition_id','record_id', 'Edition List', states={'closed': [('readonly', True)]}),
        'note': fields.text('Notes', states={'closed': [('readonly', True)]}),
        'basic_cycle1': fields.integer('Basic/Trunk', states={'closed': [('readonly', True)]}),
        'mandatory_cycle1': fields.integer('Mandatory', states={'closed': [('readonly', True)]}),
        'optional_cycle1': fields.integer('Optional', states={'closed': [('readonly', True)]}),
        'freechoice_cycle1': fields.integer('Free Choice', states={'closed': [('readonly', True)]}),
        'basic_cycle2': fields.integer('Basic/Trunk', states={'closed': [('readonly', True)]}),
        'mandatory_cycle2': fields.integer('Mandatory', states={'closed': [('readonly', True)]}),
        'optional_cycle2': fields.integer('Optional', states={'closed': [('readonly', True)]}),
        'freechoice_cycle2': fields.integer('Free Choice', states={'closed': [('readonly', True)]}),
        'degree_cycle': fields.integer('Degree Work', states={'closed': [('readonly', True)]}),
        'complement_credits': fields.integer('Complement', states={'closed': [('readonly', True)]}),
        'replacement_credits': fields.integer('Replacement', states={'closed': [('readonly', True)]}),
        'total_cycle': fields.function(_calculate_credits, method=True, type='integer', string='Total Credits', store=True, multi='sum'),
        'curr_basic1': fields.function(_calculate_credits, method=True, type='integer', string='Current Basic/Trunk', store=True,multi='sum'),
        'curr_mandatory1': fields.function(_calculate_credits, method=True, type='integer', string='Current Mandatory', store=True, multi='sum'),
        'curr_optional1': fields.function(_calculate_credits, method=True, type='integer', string='Current Optional', store=True, multi='sum'),
        'curr_freechoice1': fields.function(_calculate_credits, method=True, type='integer', string='Current Free Choice', store=True, multi='sum'),       
        'curr_basic2': fields.function(_calculate_credits, method=True, type='integer', string='Current Basic/Trunk', store=True,multi='sum'),
        'curr_mandatory2': fields.function(_calculate_credits, method=True, type='integer', string='Current Mandatory', store=True, multi='sum'),
        'curr_optional2': fields.function(_calculate_credits, method=True, type='integer', string='Current Optional', store=True, multi='sum'),
        'curr_freechoice2': fields.function(_calculate_credits, method=True, type='integer', string='Current Free Choice', store=True, multi='sum'),        
        'curr_degree': fields.function(_calculate_credits, method=True, type='integer', string='Current Degree', store=True, multi='sum'),
        'curr_complement': fields.function(_calculate_credits, method=True, type='integer', string='Current Complement', store=True, multi='sum'),
        'curr_replacement': fields.function(_calculate_credits, method=True, type='integer', string='Current Replacement', store=True, multi='sum'),
        'curr_total': fields.function(_calculate_credits, method=True, type='integer', string='Current Total', store=True, multi='sum'),
        'record_line_ids': fields.one2many('training.record.line', 'record_id', 'Record Lines', states={'closed': [('readonly', True)]}),
        'record_credits_line_ids': fields.one2many('training.record.credits.line', 'record_id', 'Session Credits', states={'closed': [('readonly', True)]}),
        'progress_rate': fields.function(_record_rate, method=True, string='Progress (%)', type='float', states={'closed': [('readonly', True)]},multi='rate'),
        'progress_rate_ing':fields.function(_record_rate, method=True, string='Progress Without Degree (%)', type='float', states={'closed': [('readonly', True)]},multi='rate'),
        'university_ids' : fields.function(_calculate_universities, type='many2many', obj='training.universities', method=True, string="Universities",),
        'state': fields.selection([
               ('opened','Opened'),
               ('pending','Pending'),
               ('solicited','Solicited'),
               ('sent_to_ministry','Sent to Ministry'),
               ('print_pending','Print pending'),
               ('sent_to_print','Sent to print'),
               ('ready_to_receive','Ready to receive'),
               ('received','Received'),
               ('closed','Closed'),
        ],'State', readonly=True),
        'average_mark': fields.function(_average_mark_calc, type='float',method=True, string='Average Mark'),
#        'session_lines': fields.function(_no_of_editions, type='float',method=True, string='Session Lines'),
        'request_date':fields.date('Request Date',readonly=True),
        'ministry_shipping_date':fields.date('Ministry Shipping Date',readonly=True),
        'ministry_reception_date':fields.date('Ministry Reception Date',readonly=True),
        'ministry_code':fields.char('Ministry Code',readonly=True,size=64),
        'printing_shipping_date':fields.date('Printing Shipping Date',readonly=True),
        'printing_reception_date':fields.date('Printing Reception Date',readonly=True),
    }
    
    _defaults = {
        'name': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'training.record'),
        'state':lambda *a:'opened',
        'average_mark': lambda *a: 0.0,
        'issecondcycle': lambda *a: False
    }
    
    def onchange_offer(self, cr, uid, ids, offer_id, context=None):
        res = {}
        if offer_id:
            offer = self.pool.get('training.offer').browse(cr, uid, offer_id)
            res = {
                'basic_cycle1': offer.basic_cycle1 or 0,
                'mandatory_cycle1': offer.mandatory_cycle1 or 0,
                'optional_cycle1': offer.optional_cycle1 or 0,
                'freechoice_cycle1': offer.freechoice_cycle1 or 0,
                'basic_cycle2': offer.basic_cycle2 or 0,
                'mandatory_cycle2': offer.mandatory_cycle2 or 0,
                'optional_cycle2': offer.optional_cycle2 or 0,
                'freechoice_cycle2': offer.freechoice_cycle2 or 0,
                'degree_cycle': offer.degree_cycle or 0,
            }
        return {'value': res }
    
    def replacement_certificate(self, cr, uid, ids, context=None):
        return True
    
    def register_payment(self, cr, uid, ids, context=None):
        return True
    
    def button_dummy(self, cr, uid, ids, context=None):
        return True
    
    #######################################################
    ## METODOS DEL WORKFLOW ##
    #######################################################

    def action_open(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'opened'})
        return True
    
    def action_pending(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'pending'})
        return True
    
    def action_request(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'solicited'})
        self.write(cr, uid, ids, {'request_date': datetime.now()})
        return True
    
    def action_send_ministry(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'sent_to_ministry'})
        self.write(cr, uid, ids, {'ministry_shipping_date': datetime.now()})
        return True
    
    def action_print_pending(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'print_pending'})
        self.write(cr, uid, ids, {'ministry_reception_date': datetime.now()})
        return True
    
    def action_sent_print(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'sent_to_print'})
        self.write(cr, uid, ids, {'printing_shipping_date': datetime.now()})      
        return True
    
    def action_ready(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'ready_to_receive'})
        self.write(cr, uid, ids, {'printing_reception_date': datetime.now()})      
        return True
    
    def action_receive(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'received'})
        return True
    
    def action_close(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'closed'})
        return True
    
training_record()
