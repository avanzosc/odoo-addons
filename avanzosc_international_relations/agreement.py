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

class agreement(osv.osv):
    
    _name = 'agreement'
    _description = 'Agreement'
    _rec_name = 'registration_number'
    
    _columns = {
            
            'registration_number': fields.char('Registration Nº', size=64, required=True),
            'summary':fields.text('Summary'),
            'institution_id': fields.many2one('res.partner', 'Institution'),
            'institution_type': fields.selection([('university','University'),('company','Company')],'Institution Type'),
            'still_stands':fields.boolean('Still Stands'),
            'not_working':fields.boolean('Not Working'),
            'practical_effect':fields.boolean('Practical Effect this year'),
            'extensions':fields.char('Extensions',size=128),
            'subject1': fields.char('Subject 1', size=128),
            'subject2': fields.char('Subject 2', size=128),  
            'subject3': fields.char('Subject 3', size=128),  
            'subject4': fields.char('Subject 4', size=128),  
            'subject5': fields.char('Subject 5', size=128),
            'erasmus':fields.boolean('Erasmus'),
            'erasmus_code': fields.char('erasmus_code', size=64),
            'agreement_date':fields.date('Agreement Date'),
            'comments':fields.text('Comments'),
            'offer_ids': fields.many2many('training.offer','rel_agreement_offer','agreement_id','offer_id','Offers'),  
    }
#    _defaults = {
#        'registration_number': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'agreement'),
#    }
     
agreement()

class res_partner(osv.osv):
    
    _inherit = "res.partner"
    _columns = {
                'agreement_ids':fields.one2many('agreement', 'institution_id', 'Agreements'),
                'institution':fields.boolean('Institution'),
        }
res_partner()

class training_offer(osv.osv):
    
    _inherit = 'training.offer'
       
    _columns = {
                'agreement_ids': fields.many2many('agreement','rel_agreement_offer','offer_id','agreement_id','Agreements'),
         
    } 
    
training_offer() 


