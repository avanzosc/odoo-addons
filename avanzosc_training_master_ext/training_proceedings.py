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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from osv import osv
from osv import fields
from datetime import datetime
from tools.translate import _

class training_court_proceedings(osv.osv):
    
    #iker
    _name = 'training.court.proceedings'
    _description = 'Groups for Proceedings'
    _rec_name="name"
    
    _columns = {
        'code': fields.char ('Code', size = 64),
        'name': fields.char('Name', size = 64),
        }
    
training_court_proceedings()

class training_group_proceedings(osv.osv):
    #iker
    _name = 'training.group.proceedings'
    _description = 'Groups for Proceedings'
    _rec_name="name"
    
    _columns = {
        'code': fields.char ('Code', size = 64),
        'name': fields.char('Name', size = 64),
        }
    
training_group_proceedings()

class training_month_notice(osv.osv):
    '''
    Objeto en el que definimos el mes de las Actas
    '''
    #iker
    _name = 'training.month.notice'
    _description = 'Month of notice'
    _rec_name="name"
    
    _columns = {
        'code': fields.char ('Code', size = 64),
        'name': fields.char('Name', size = 64),
        'date':fields.date('Fecha de acta'),
        }
    
training_month_notice()

class training_type_proceedings(osv.osv):
    '''
    Objeto en el que decidimos el tipo de Acta
    '''
    #iker
    _name = 'training.type.proceedings'
    _description = 'Type of Procedings'
    _rec_name="name"
    
    _columns = {
        'code': fields.char ('Code', size = 64),
        'name': fields.char('Name', size = 64),    
        }    
training_type_proceedings()

class training_proceedings(osv.osv):
    #iker
    _name = 'training.proceedings'
    _description = 'Proceedings'
    _rec_name="year"
    def create_new_proceeding(self, cr, uid, ids, context=None):
        #iker
        '''
        Creamos una segunada acta automatica
        -Si se ha suspendido se añade la segunda convocatoria a ese acta
        -Si se ha aprobado se deja inactiva la segunda convocatoria de ese alumno en esa asignatura :)
        '''
        ##########################################################
        # OBJETOS
        ##########################################################
        proceedings_obj = self.pool.get ('training.proceedings')
        record_line_obj = self.pool.get('training.record.line')
        ##########################################################
        # ARRAYS
        ##########################################################
        student_items = []
        ##########################################################
        
        #proceedings = proceedings_obj.browse(cr, uid, context['active_id'])
        for proceedings in self.browse(cr, uid, ids, context):
            offer = proceedings.offer_id.id
            seance = proceedings.seance_id.id
            group = proceedings.group_proceeding_id.id
            type = proceedings.type_proceeding_id.id
            month = proceedings.month_notice_id.id
            year = proceedings.year
            court = proceedings.act_court
            
        id_proceeding = proceedings_obj.search (cr, uid, [('offer_id','=',offer),('seance_id','=',seance),('group_proceeding_id','=',group),('type_proceeding_id','=',type),('month_notice_id','=',month),('year','=',year),('act_court','=',court)])
        #id_proceeding = ids
        
        #cambiamos los valores de los campos states en el caso de que se apruebe la asignatura.
        lines_id = record_line_obj.search(cr, uid,[('proceeding_ids','in',id_proceeding)]) 
        for lines in record_line_obj.browse(cr, uid, lines_id, context=None):
            student = lines.student_id.id
            seance = lines.seance_id.id
            mark = lines.mark
            call = lines.call
            
            extra_record_lines_ids = record_line_obj.search (cr, uid, [('student_id','=',student),('seance_id','=',seance),('call','>',call),('state','=','not_sub')]) 
            
            if extra_record_lines_ids:
                if mark < 5:
                    student_items.append(extra_record_lines_ids[0])
                    
                elif mark >= 5:
                    record_line_obj.write(cr, uid,extra_record_lines_ids,{'state':'no_used'},context)
                    
        #Creamos nuestro nuevo objeto.
            
        val_proceedings = {
                   'offer_id': offer,
                   'seance_id': seance,
                   'type_proceeding_id': type,
                   'group_proceeding_id': group,
                   'year': year,
                   'act_court':court,
                   }
        new_proceedings_obj = proceedings_obj.create(cr, uid, val_proceedings, context)
            
#            for registros in record_line_obj.browse(cr, uid, student_items, context):
#                   record_line_obj.write(cr,uid,registros,{'proceeding_ids':new_proceedings_obj},context)
                   
        record_line_obj.write(cr,uid,student_items,{'proceeding_ids':new_proceedings_obj},context)
    
    
    def _count_students(self, cr, uid, ids, name, args,  context=None):
        #iker
        '''
        Contamos numero de alumnos por acta
        '''
        ##########################################################
        # OBJETOS
        ##########################################################
        proceedings_obj = self.pool.get ('training.proceedings')
        record_line_obj = self.pool.get('training.record.line')
        ##########################################################
        # ARRAYS
        ##########################################################
        res = {} 
        ##########################################################
        #proceedings = self.browse(cr, uid, ids[0]) 
        for proceedings in ids:
            line_list = record_line_obj.search(cr, uid, [('proceeding_ids', '=',proceedings)])
            if line_list:
                count = len(line_list)
                #print count
            else:
                count = 0
                     
            res[proceedings]=count
        return res
       
 
    _columns = {   
        'offer_id':fields.many2one('training.offer','Offer',states={'close': [('readonly', True)]}), 
        'seance_id':fields.many2one('training.seance','Seances',states={'close': [('readonly', True)]}),
        'type_proceeding_id':fields.many2one('training.type.proceedings','Type Proceeding',states={'close': [('readonly', True)]}),
        'group_proceeding_id':fields.many2one('training.group.proceedings','Group',states={'close': [('readonly', True)]}),
        'month_notice_id':fields.many2one('training.month.notice','Month',states={'close': [('readonly', True)]}),
        'year': fields.integer('Year',required=True,states={'close': [('readonly', True)]}),
        'record_line_ids': fields.one2many('training.record.line','proceeding_ids','Record Lines',states={'close': [('readonly', True)]}),
        'contact': fields.many2many('res.partner.contact','rel_proceeding_contact','proceeding_id','contact_id','Teacher',states={'close': [('readonly', True)]}),
        'court': fields.many2many('res.partner.contact','rel_proceeding_court','proceeding_id','contact_id','Court',states={'close': [('readonly', True)]}),
        'act_court': fields.boolean('court',states={'close': [('readonly', True)]}),
        'count_student': fields.function(_count_students,type='integer', method=True, string='Num. Students',states={'close': [('readonly', True)]}),
        'notes': fields.text('Notes',states={'close': [('readonly', True)]}),
        'state': fields.selection([
                                ('draft', 'Draft'),
                                ('inproces', 'In Process'),
                                ('close', 'Close'),],'State', required=True),             
        }
    _defaults ={
        'year': lambda *a:  int(datetime.now().year),
        'state': lambda *a: 'draft',
                } 
    
    
        
    def clear_selected_files(self, cr, uid, ids, context=None):
        #iker
        '''
        Limpiamos las lineas que nos hayamos cogido por error.
        '''
        ##########################################################
        # OBJETOS
        ##########################################################
        record_line_obj = self.pool.get('training.record.line')
        proceedings_obj = self.pool.get ('training.proceedings')
        ########################################################## 
        proceedings = proceedings_obj.browse(cr, uid, context['active_id'])
        
        for all_lines in proceedings_obj.browse(cr, uid, ids):
            if all_lines:
                for lines in all_lines.record_line_ids:
                    if lines.clear:
                        record_line_obj.write(cr, uid, lines.id,{'proceeding_ids':False,'clear':False})
            else:
                 raise osv.except_osv(_('Error!'),_('No line(s) selected to erase!'))
        return True
    
    #######################################################
    ## METODOS DEL WORKFLOW ##
    #######################################################

    def action_draft(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
    def action_inproces(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'inproces'})
        return True  
    
    def action_close(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'close'})
        return True  
    
training_proceedings()

class training_group_of_proceedings(osv.osv):
    _name = 'training.group.of.proceedings'
    _description = 'Group of proceeding to unify same lecture an teacher'
    
    _columns = {
            'name': fields.char('Name',size=64),
            'info': fields.text('Info'), 
            'proceeding_ids': fields.many2many('training.proceedings','rel_proceedings','group_of_proceeding_id','proceeding_id','Group Proceedings'),  
    }
training_group_of_proceedings()

class res_partner_contact(osv.osv):
    _inherit = 'res.partner.contact'
    _columns = {
        'proceeding_ids': fields.many2many('training.proceedings','rel_proceeding_contact','contact_id','proceeding_id','Proceedings'),
    }
res_partner_contact()

class training_record_line(osv.osv):
    _inherit='training.record.line'
    _columns = {
                'proceeding_ids': fields.many2one('training.proceedings','Proceedings'),
            }
training_record_line()
