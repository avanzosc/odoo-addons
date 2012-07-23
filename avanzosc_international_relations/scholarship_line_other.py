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

class scholarship_line_other(osv.osv):
    
    _name = 'scholarship.line.other'
    _description = 'Scholarship Line Other'
    
    _columns = {
            
            'scholarship_id':fields.many2one('scholarship','Scholarship'),
            'mode':fields.related('scholarship_id','scholarship_mode',type='selection',selection=[('entry','Entry'),('output','Output'),('others','Others')],string='Mode',store=True),
            'contact_id':fields.many2one('res.partner.contact','Contact'),
            'country_id':fields.many2one('res.country','Country'),
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
                    
     
scholarship_line_other()

class agreement(osv.osv):
    
    _inherit = 'agreement'
    _description = 'Agreement'
    
    _columns = {
            
            'scholarship_des_other_ids':fields.one2many('scholarship.line.other','destination_id','Scholarship Other Lines(Destination)'),
            'scholarship_sou_other_ids':fields.one2many('scholarship.line.other','source_id',"Scholarship Other Lines(Source)"),
                    
    }
     
agreement()

class scholarship(osv.osv):
 
    _inherit = 'scholarship'
    
    _columns = {
                
            'scholarship_line_other_ids':fields.one2many('scholarship.line.other', 'scholarship_id', 'Scholarships Lines(Others)'),
    }
scholarship()
