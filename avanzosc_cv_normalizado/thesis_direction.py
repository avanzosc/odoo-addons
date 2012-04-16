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

class thesis_direction(osv.osv):
    _name = 'thesis.direction'
    _description = 'thesis direction'
    
    _columns = {
            
            'contact_id': fields.many2one('res.partner.contact', 'Contact'),
            'work_title':fields.char('Work Title', size=128),
            'project_type':fields.char('Project Type', size=128),
            'thesis_codirector':fields.char('Thesis Codirector', size=128),
            'university':fields.char('University', size=128),
            'alumn':fields.char('Alumn', size=128),
            'mark':fields.float('Mark'),
            'reading_date':fields.date('Reading Date'),
            'mention_date':fields.date('Mention Date'),
            'quality_mention':fields.boolean('Quality Mention'),
            
    }
thesis_direction()
