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
    "name": "Avanzosc training international relations",
    "version": "1.0",
    "depends": ["base", 
                "base_contact",
                "avanzosc_training_master_ext",
                ],
    "author": "AvanzOSC",
    "category": "Training Course",
    "description": """
    This module provide :
    """,
    "init_xml": [],
    'update_xml': ["training_international_relations.xml",
                   "training_international_relations_sequence.xml",
                   "workflow_scholarship.xml",
                   "workflow_scholarship_line_student.xml",
                   "workflow_scholarship_line_practice.xml",
                   "workflow_scholarship_line_teacher.xml",
                   "workflow_scholarship_line_other.xml",
                   "workflow_practice_line.xml"
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}