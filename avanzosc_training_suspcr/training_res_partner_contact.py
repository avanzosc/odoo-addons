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
from datetime import datetime, timedelta

class res_partner_contact(osv.osv):

    _inherit = 'res.partner.contact'
 
    def _no_of_sales(self, cr, uid, ids, name, args, context=None):
        res = {}
        sum=0
        for contact in self.browse(cr, uid, ids, context=context):
            sum = len(contact.sale_ids or [])
            res[contact.id]=sum        
        return res
    
#    Calcular edad mediante función

    def _age(self, cr, uid, ids, name, args, context=None):
        res = {}
        age_int=0
        for contact in self.browse(cr, uid, ids, context=context):
            if contact.birthdate:
                date=int(datetime.now().year)
                age=contact.birthdate
                age_str=str(age)
                age_split=age_str.split('-')
                age_year=age_split[0]
                age_int=date-int(age_year)
            res[contact.id]=age_int
        return res
    
#    Calcular edad mediante onchange
#    def onchange_birthdate(self, cr, uid, ids, birthdate, context=None):
#        age_int=0
#        if birthdate:
#            date=int(datetime.now().year)
#            age=birthdate
#            age_str=str(age)
#            age_split=age_str.split('-')
#            age_year=age_split[0]
#            age_int=date-int(age_year)
#        res = {
#               'student_age': age_int,
#        }
#        return {'value': res}
    
    _columns = {
            'record_lines_id':fields.one2many('training.record.line','partner_id','Record Lines'),
            'records':fields.one2many('training.record','student_id','Records',readonly=True),
            'sale_ids':fields.one2many('sale.order','contact_id','Sales'),
            'no_of_sales':fields.function(_no_of_sales, type='float',method=True, string='Sales'),
            'student_age':fields.function(_age, type='integer',method=True, string='Student Age'),
#            'student_age':fields.integer('Student Age'),
            
        }
res_partner_contact()

class training_record_line(osv.osv):
     _inherit = 'training.record.line'
 
     _columns = {
            'partner_id':fields.related('record_id','student_id',type = 'many2one',relation = 'res.partner.contact',string = 'name', store = True,readonly = True),
        }
training_record_line()

class sale_order(osv.osv):
     _inherit = 'sale.order'
 
     _columns = {
        'sales': fields.related('contact_id','no_of_sales',type='float', string='Sales',store=True),
        }
sale_order()    
