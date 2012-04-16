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

class teaching(osv.osv):
    _name = 'teaching'
    _description = 'teaching'
    
    _columns = {
            
            'contact_id': fields.many2one('res.partner.contact', 'Contact'),
            'name':fields.char('Name', size=128),
            'category':fields.char('Category', size=128),
            'program_type':fields.char('Program Type', size=128),
            'teaching_type':fields.char('Teaching Type', size=128),
            'subject_type':fields.char('Subject Type', size=128),
            'titulation':fields.char('Titulation', size=128),
            'course':fields.integer('Course'),
            'course_type':fields.selection([('hours','Hours'),('credits','Credits')],'Course Type'),
            'duration':fields.integer('Duration'),
            'entity':fields.char('Entity', size=128),
            'department':fields.char('Department', size=128),
            'city':fields.char('City', size=128),
            
    }
teaching()