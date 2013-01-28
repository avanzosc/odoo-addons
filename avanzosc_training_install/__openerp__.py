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
    "name": "Training Install",
    "version": "1.0",
    "depends": [
                "avanzosc_crm_training_subscription",
                "avanzosc_training_contact",
                "avanzosc_international_relations",
                "avanzosc_training_certificate",
                "avanzosc_training_comission_designation",
                "avanzosc_training_extructura_auxiliar_ucav",
                "avanzosc_training_inscription_real",
                "avanzosc_training_instance",
                "avanzosc_training_suspcr",
                "base_contact_crm"
                ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.com",
    "category": "Training Install Module",
    "description": """
    This module provide :
        * Installation of all modules
    """,
    "init_xml": [],
    'update_xml': [
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}