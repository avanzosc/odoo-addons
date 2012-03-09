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

class res_partner_contact(osv.osv):

    _inherit = 'res.partner.contact'
 
    _columns = {
            'record_lines_id':fields.one2many('training.record.line','partner_id','Record Lines'),
            'records':fields.one2many('training.record','student_id','Records',readonly=True),
        }
res_partner_contact()

class training_record_line(osv.osv):
     _inherit = 'training.record.line'
 
     _columns = {
            'partner_id':fields.related('record_id','student_id',type = 'many2one',relation = 'res.partner.contact',string = 'name', store = True,readonly = True),
        }
training_record_line()    
