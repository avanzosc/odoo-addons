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
    _name = 'training.calendar'

    _columns = {
	    'name': fields.char('Name', size=32, required=True),	
        'date_from' : fields.datetime('Date From', required=True, help="The data when course begins"),
        'date_end' : fields.datetime('Date End', required=True, help="The data when course ends"),    
     }

training_course_calendar()

