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
from tools.translate import _


class wiz_find_student(osv.osv_memory):
    '''
    Wizard para la seleccion de Alumnos.
    '''
    _name = 'wiz.find.student'
    _description = 'wiz to add a student to a proceedings'
 
    _columns = {
            'wiz_line': fields.one2many('wiz.line.selected','wiz_id','Wiz'),
        
        }
    def default_get(self,cr, uid, ids, context=None):
        '''
        Cargamos los estudiantes que cumplan una titulación y una seance.
        Por cada ID de Record, Miramos las lines que tiene, si tiene una sola linea no problem.
        Si tiene más de una lina  cargamos la del call mas pequeño.
        '''
        ##########################################################
        # ARRAYS
        ##########################################################
        student_items = []
        values= {}
        ##########################################################
        # OBJETOS
        ##########################################################
        record_obj = self.pool.get('training.record')
        record_line_obj = self.pool.get('training.record.line')
        proceedings_obj = self.pool.get ('training.proceedings')
        wiz_line_selected_obj = self.pool.get ('wiz.line.selected')
        ##########################################################
        
        proceedings = proceedings_obj.browse(cr, uid, context['active_id'])
        offer = proceedings.offer_id.id or 0
        seance = proceedings.seance_id.id or 0
        group = proceedings.group_proceeding_id.id or 0
              
        if offer !=0 or seance !=0:
            record_ids = record_obj.search(cr,uid,[('offer_id','=',offer)])
            #Recorremos los objetos uno a uno.
            for record_id in record_ids:
                if record_id:
                    record_line_ids = record_line_obj.search(cr,uid,[('seance_id','=', seance),('record_id','=',record_id),('proceeding_ids','=',False),('state','=','not_sub')])
                    if len( record_line_ids) > 1:
                        selected = record_line_obj.browse(cr,uid,record_line_ids,context)[0]
                        for record_lines in record_line_obj.browse(cr,uid,record_line_ids,context):
                            if record_lines.call < selected.call: 
                                selected = record_lines
                            else:
                                selected = selected
                        #Creamos el objeto y lo añadimos al array
                        var = ({
                            'wiz_id':1,
                            'id_line':selected.id,
                            'name':selected.student_id.id,
                            'chk':True,
                            })
                        student_items.append(var)        
                        
                    elif len(record_line_ids) == 1:
                        for record_lines in record_line_obj.browse(cr,uid,record_line_ids,context):
                            var = ({
                                    'wiz_id':1,
                                    'id_line':record_lines.id,
                                    'name':record_lines.student_id.id,
                                    'chk':True,
                                })
                            student_items.append(var)
        else:
            raise osv.except_osv(_('Error!'),_('Offer  or seance is/are null'))
        
        values.update({'wiz_line':student_items})
        return values
    
    def insert_charge(self, cr, uid, ids, context=None):
        '''
        Cargamos el student_items en las lineas de 
        '''   
        ##########################################################
        # OBJETOS
        ##########################################################
        record_obj = self.pool.get('training.record')
        record_line_obj = self.pool.get('training.record.line')
        proceedings_obj = self.pool.get ('training.proceedings')
        ##########################################################
        proceedings = proceedings_obj.browse(cr, uid, context['active_id'])
        
        for wiz in self.browse(cr, uid, ids):
            if wiz.wiz_line:
                for w_line in wiz.wiz_line:
                    if w_line.chk:
                        record_line_obj.write(cr,uid,w_line.id_line.id,{'proceeding_ids':proceedings.id})
        return {'type': 'ir.actions.act_window_close'}
                      
wiz_find_student()

class wiz_line_selected(osv.osv_memory):
    
    _name = 'wiz.line.selected'
    _description = 'wiz to add a student to a proceedings'
    _columns = {
            'wiz_id': fields.many2one('wiz.find.student','wiz_id'),
            'name':fields.many2one('res.partner.contact','Name'),
            'id_line': fields.many2one('training.record.line','Id Linea'),
            'chk':fields.boolean('chk'),
        }
wiz_line_selected()