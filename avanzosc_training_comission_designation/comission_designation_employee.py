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

class comission_designation_employee(osv.osv):
    _name = 'comission.designation.employee'
    _description = 'comission/designation employee'
    
    _columns = {
            
            'employee_id':fields.many2one('hr.employee','Employee'),
            'hr_job_id':fields.many2one('hr.job','Hr job'),
            'init_date':fields.date('Init Date'),
            'end_date':fields.date('End Date'),
            'expiration_date':fields.date('Expiration Date'),
            'active':fields.boolean('Active'),
    }
    _defaults = {
                 'active':lambda *a: 1,
                 }
comission_designation_employee()
