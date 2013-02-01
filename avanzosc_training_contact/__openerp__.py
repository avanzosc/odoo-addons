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
{
    "name": "Avanzosc training contact",
    "version": "1.0",
    "depends": [
                "base", 
                "base_contact",
                "avanzosc_cv_normalizado",
                "avanzosc_training_master_ext",
                ],
    "author": "AvanzOSC",
    "category": "RRHH",
    "description": """
    This module provide :
    """,
    "init_xml": [],
    'update_xml': [
                   "training_city_view.xml",
                   "training_identification_type_view.xml",
                   "training_left_reason_view.xml",
                   "training_parent_studies_view.xml",
                   "training_specialities_view.xml",
                   "training_ucav_access_type_view.xml",
                   "training_university_access_type_view.xml",
                   "training_workskills_view.xml",
                   "authorized_person_view.xml",
                   "training_res_partner_contact_sequence.xml",
                   "training_res_partner_contact_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}