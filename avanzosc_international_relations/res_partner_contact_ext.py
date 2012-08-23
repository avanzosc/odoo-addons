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
            'scholarship_line_student_ids':fields.one2many('scholarship.line.student', 'contact_id', "Scholarship Lines Students"),
            'scholarship_line_practice_ids':fields.one2many('scholarship.line.practice', 'contact_id', "Scholarship Lines Practice"),
            'scholarship_line_teacher_ids':fields.one2many('scholarship.line.teacher', 'contact_id', "Scholarship Lines Teacher"),
            'scholarship_line_other_ids':fields.one2many('scholarship.line.other', 'contact_id', "Scholarship Lines Other"),
            'practice_ids':fields.one2many('practice', 'student_id', "Practice Lines"),
        }
res_partner_contact()
