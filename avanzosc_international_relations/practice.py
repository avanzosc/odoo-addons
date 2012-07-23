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

class practice(osv.osv):
    
    _name = 'practice'
    _description = 'Practice'
    
    _columns = {
            
            'name': fields.char('Name', size=64, required=True),
            'alumn_id':fields.many2one('res.partner.contact','Alumn'),
            'company_id':fields.many2one('agreement','Company'),
            'description':fields.char('Description', size=64),
            'requirements':fields.text('Requirements'),
            'init_date':fields.date('Estimated Init Date'),
            'end_date':fields.date('Estimated End Date'),
            'sub_company': fields.char('Subcompany', size=64),
            'tutor': fields.char('Tutor', size=64),
            'evaluation': fields.char('Evaluation', size=64),
            'state': fields.selection([
               ('draft','Draft'),
               ('accepted','Accepted'),
               ('refused','Refused'),
               ('completed','Completed'),
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
    
    def action_complete(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'completed'})
        return True
     
practice()

class agreement(osv.osv):
    
    _inherit = 'agreement'
    _description = 'Agreement'
    
    _columns = {
            
            'practice_ids':fields.one2many('practice','company_id','Practice Lines'),                    
    }
     
agreement()