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

class res_partner_contact(osv.osv):
    
    _inherit = 'res.partner.contact'
    _description = 'res.partner.contact'
    
 
    _columns = {
                
            'lastname_two': fields.char('Last Name 2', size=64),
            'identification_doc':fields.char('Identification Document', size=64),
            'sex':fields.selection([('man','Man'),('woman','Woman')],'Sex'),
            'address':fields.char('Contact Address', size=256),
            'zip_code': fields.integer('Zip Code'),
            'city':fields.char('Contact City', size=32),
            'country':fields.many2one('res.country','Country'),
            'state_id':fields.many2one('res.country.state','State'),
            'community':fields.char('Community', size=32),
            'telephone':fields.char('Telephone', size=64),
            'fax':fields.char('Fax', size=64),
            'position_ids': fields.one2many('position', 'contact_id', "Positions"),
            'degree_ids': fields.one2many('degree', 'contact_id', "Degrees"),
            'doctorate_ids': fields.one2many('doctorate', 'contact_id', "Doctorates"), 
            'course_ids': fields.one2many('course', 'contact_id', "Courses"),
            'teaching_ids':fields.one2many('teaching', 'contact_id', "Teachings"),
            'thesis_direction_ids':fields.one2many('thesis.direction','contact_id',"Thesis Directions"),
            'teaching_material_ids':fields.one2many('teaching.material','contact_id',"Teaching Materials"),
            'congress_ids':fields.one2many('congress','contact_id',"Congresses"),
            'innovation_project_ids':fields.one2many('innovation.project','contact_id',"Innovation Projects"),
            'project_participation_ids':fields.one2many('project.participation','contact_id',"Project Participations"),
            'artistic_work_ids':fields.one2many('artistic.work','contact_id',"Artistic Works"),
            'publication_ids':fields.one2many('publication','contact_id',"Publications"),
            'congress_work_ids':fields.one2many('congress.work','contact_id',"Congress Works"),
            'course_work_ids':fields.one2many('course.work','contact_id',"Course Works"),
            'other_activity_ids':fields.one2many('other.activity','contact_id',"Other Activities"),
            'rd_center_stay_ids':fields.one2many('rd.center.stay','contact_id',"R+D Center Stays"),
            'aid_ids':fields.one2many('aid','contact_id',"Aids"),
            'prize_ids':fields.one2many('prize','contact_id',"Prizes"),
            'recognition_ids':fields.one2many('recognition','contact_id',"Recognitions"),
            'other_merit_ids':fields.one2many('other.merit','contact_id',"Other Merits"),
                 
    }
    
    
res_partner_contact()

class res_country(osv.osv):
 
    _inherit = 'res.country'
    
    _columns = {
                
        'contact_ids': fields.one2many('res.partner.contact', 'country','Contacts'),
    }
res_country()

class res_country_state(osv.osv):
    
    _inherit = 'res.country.state'
    
    _columns = {
            
        'contact_ids':fields.one2many('res.partner.contact', 'state_id', "Contacts"),

        }
res_country_state()