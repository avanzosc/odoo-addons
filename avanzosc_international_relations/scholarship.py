# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    Copyright (C) 2012 Avanzosc (http://Avanzosc.com). All Rights Reserved
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

class scholarship(osv.osv):
    
    _name = 'scholarship'
    _description = 'Scholarship'
    
    def _check_mode(self, cr, uid, ids, context=None):
        #iker
        for scholarship in self.browse(cr,uid,ids):
            action = True
            mode=scholarship.scholarship_mode
            print mode
            for line in scholarship.scholarship_line_student_ids:
                print "origen student:"
                print line.source_id
                print "destino student:"
                print line.destination_id
                if mode=='entry':
                    if not line.source_id:
                        action = False
                elif mode=='output':
                    if not line.destination_id:
                        action = False
            for line in scholarship.scholarship_line_teacher_ids:
                print "origen teacher:"
                print line.source_id
                print "destino teacher:"
                print line.destination_id
                if mode=='entry':
                    if not line.source_id:
                        action = False
                elif mode=='output':
                    if not line.destination_id:
                        action = False
            for line in scholarship.scholarship_line_practice_ids:
                print "origen practice:"
                print line.source_id
                print "destino practice:"
                print line.destination_id
                if mode=='entry':
                    if not line.source_id:
                        action = False
                elif mode=='output':
                    if not line.destination_id:
                        action = False
            for line in scholarship.scholarship_line_other_ids:
                print "origen other:"
                print line.source_id
                print "destino other:"
                print line.destination_id
                if mode=='entry':
                    if not line.source_id:
                        action = False
                elif mode=='output':
                    if not line.destination_id:
                        action = False
        return action     
    
    _columns = {
            
            'name': fields.char('Name', size=64, required=True),
            'init_date':fields.date('Request Init Date'),
            'end_date':fields.date('Request End Date'),
            'granted_amount': fields.char('Granted Amount', size=64),
            'scholarship_type_id':fields.many2one('scholarship.type','Scholarship Type'),
            'scholarship_mode':fields.selection([('entry','Entry'),('output','Output'),('others','Others')],'Scholarship Mode'),
            'state': fields.selection([
               ('draft','Draft'),
               ('active','Active'),
               ('closed','Closed'),
               ],'State', readonly=True),
    }
    
    _defaults = {
        'state':lambda *a:'draft',
    }
    
    _constraints = [
                 (_check_mode,'Error: If scholarship mode is entry, source is required in lines. If scholarship mode is output, destination is required in lines.',[]),                   
                 ]
    
    #######################################################
    ## METODOS DEL WORKFLOW ##
    #######################################################
    
    def action_draft(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
    def action_active(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'active'})
        return True
    
    def action_close(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'closed'})
        return True
     
scholarship()

class scholarship_type(osv.osv):
 
    _inherit = 'scholarship.type'
    
    _columns = {
                
                'scholarship_ids':fields.one2many('scholarship', 'scholarship_type_id', 'Scholarships'),
    }
scholarship_type()
