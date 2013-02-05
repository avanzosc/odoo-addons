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

class scholarship_line_student(osv.osv):
    
    _name = 'scholarship.line.student'
    _description = 'Scholarship Line Student'
    
    _columns = {
            
            'scholarship_id':fields.many2one('scholarship','Scholarship'),
            #'mode':fields.related('scholarship_id','scholarship_mode',type='selection',selection=[('entry','Entry'),('output','Output'),('others','Others')],string='Mode',store=True),
            'contact_id':fields.many2one('res.partner.contact','Contact'),
            'country_id':fields.many2one('res.country','Country'),
#            'titulation_id':fields.many2one('training.record','Titulations'),
            'titulation_id':fields.related('contact_id','records',type='one2many',relation='training.record',string='Titulations'),
#            'average_mark':fields.float('Average Mark'),
            'mark':fields.related('titulation_id','average_mark',type='float',string='Average Mark',store=True),
            'destination_id':fields.many2one('agreement','Destination'),
            'source_id':fields.many2one('agreement','Source'),
            'amount':fields.float('Amount'),
            'departure_date':fields.date('Estimated Departure Date'),
            'arrival_date':fields.date('Estimated Arrival Date'),
            'notes':fields.text('Notes'),
            'scholarship_type':fields.related('scholarship_id','scholarship_type_id',type='many2one',relation='scholarship.type',string='Scholarship Type',store=True),
            'state': fields.selection([
               ('draft','Draft'),
               ('accepted','Accepted'),
               ('refused','Refused'),
               ],'State', readonly=True),
    }
    
    _defaults = {
        'state':lambda *a:'draft',
    }
    
    
    #######################################################
    ## METODOS DEL WORKFLOW ##
    #######################################################
    
    def action_draft(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
    def action_accept(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'accepted'})
        return True
    
    def action_refuse(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'refused'})
        return True
                    
     
scholarship_line_student()

class agreement(osv.osv):
    
    _inherit = 'agreement'
    _description = 'Agreement'
    
    _columns = {
            
            'scholarship_des_student_ids':fields.one2many('scholarship.line.student','destination_id','Scholarship Student Lines(Destination)'),
            'scholarship_sou_student_ids':fields.one2many('scholarship.line.student','source_id',"Scholarship Student Lines(Source)"),
                    
    }
     
agreement()

class scholarship(osv.osv):
 
    _inherit = 'scholarship'
    
    _columns = {
                
        'scholarship_line_student_ids':fields.one2many('scholarship.line.student', 'scholarship_id', 'Scholarships Lines(Students)'),
    }
scholarship()
