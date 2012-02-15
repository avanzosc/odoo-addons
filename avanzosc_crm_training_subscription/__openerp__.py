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

{
    "name": "Avanzosc CRM Call Extension",
    "version": "1.0",
    "depends": ["base",
                "crm",
                "training",
                ],
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "category": "Custom Module",
    "website" : "www.avanzosc.com",
    "description": """
    This module provide 1 buttons to record:
        * Training Inscription from opportunity
           
    The state of the new inscription will be 'draft' and as a responsible of the case, the corresponding responsible of the suscriptions team will be stablished as default.
    """,
    "init_xml": [],
    'update_xml': ["wizard/crm_opportunity_to_suscription_view.xml",
                   "crm_opportunity_view.xml",
                   "Iniciativa_contacto_add_view.xml",
                   "presubscription_sequence.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}