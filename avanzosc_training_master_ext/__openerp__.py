
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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
    "name": "Training Extension",
    "version": "1.0",
    "depends": ["base",
                "training",
                "sale"
                ],
    "author": "AvanzOSC",
    "category": "Training Course",
    "description": """
        -Customised fields in Subjects.
        -Add university,source to trainig.subscription view
        -ADD universities,Sources and Coursenum tables.
        -ADD mantenance view for universities,Sources and Coursenum.
        -ADD views for universities,Sources and Coursenum.
        -CREATE Training Record from Sale Order & Saler Order Lines.
    """,
    "init_xml": [],
    'update_xml': [
                   'training_master_ext_view.xml',
                   "training_record_view.xml",
                   'subscription_university_view.xml',
                   'subscription_line_add_numcourse.xml',
                   'training_suspcr_sequence.xml',
                   'training_titles_view.xml',
                   'training_universities_view.xml',
                   'training_source_view.xml',
                   'training_coursenum_view.xml',
                   'training_credit_prices_view.xml',
				   'wizard/create_record_lines_view.xml',
				  ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
