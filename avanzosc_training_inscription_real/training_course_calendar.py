# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

import time

from crm import crm
from osv import fields, osv
from tools.translate import _

class training_course_calendar(osv.osv):
    '''
    Calendario escolar en el cual se define de cada año lectivo
    su inicio de semestre y fin de semestre.
    '''
    _name = 'training.course.calendar'

    _columns = {
	    'name': fields.char('Name', size=32, required=True),	
        'first_semester_start' : fields.datetime('First semester start', required=True, help="The data when course begins"),
        'first_semester_end': fields.datetime('First semester end', required=True, help = "The first semester end date of the planned session"),
        'second_semester_start': fields.datetime('Second semester start', required=True, help = "The second semester start date of the planned session"),
        'second_semester_end' : fields.datetime('Second semester end', required=True, help="The data when course ends"),    
     }

training_course_calendar()

