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
