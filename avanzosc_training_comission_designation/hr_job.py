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

class hr_job(osv.osv):
    
    def _no_of_employee(self, cr, uid, ids, name, args, context=None):
        res = {}
        sum=0
        for job in self.browse(cr, uid, ids, context=context):
            sum = len(job.comission_designation_employee_ids or [])+len(job.comission_designation_contact_ids or [])
            for employee in job.comission_designation_employee_ids:
                if employee.end_date != False:
                    sum=sum-1 
            for contact in job.comission_designation_contact_ids:
                if contact.end_date != False:
                    sum=sum-1
            res[job.id]=sum        
        return res
    
    _inherit = 'hr.job'
    _description = 'hr job'
 
    _columns = {    
            'no_of_employee': fields.function(_no_of_employee, method=True, string="No of Employees", help='Number of employees with that job.'),
            'comission_designation_contact_ids':fields.one2many('comission.designation.contact','hr_job_id',"Comission/Designation Contacts"),
            'comission_designation_employee_ids':fields.one2many('comission.designation.employee','hr_job_id',"Comission/Designation employees"),
        }
    
hr_job()    
