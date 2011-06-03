# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc, OpenERP Professional Services   
#    Copyright (C) 2010-2011 Avanzosc S.L (http://www.avanzosc.com). All Rights Reserved
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
    "name": "Avanzosc CRM Call Extension",
    "version": "1.0",
    "depends": ["base",
                "crm",
                "crm_helpdesk"
                ],
    "author": "Avanzosc S.L. (Urtzi Odriozola)",
    "category": "Custom Module",
    "description": """
    This module provide 2 buttons to record:
        * Technical incidence from the CRM input form.
        * Administrative incidence from the CRM input form
    
    The state of the new incidence will be 'pending' and as a responsible of the case, the corresponding responsible of the technical/administrative team will be stablished as default.
    """,
    "init_xml": [],
    'update_xml': ["wizard/crm_phonecall_to_technicalcase_view.xml",
                   "wizard/crm_phonecall_to_admincase_view.xml",
                   "crm_phonecall_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}