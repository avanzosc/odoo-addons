# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
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
    "name" : "purchase_triple_validation",
    "version" : "1.0",
    "category": 'Custom Modules/Sales & Purchases',
    "depends" : ["base","purchase", "purchase_double_validation"],
    "author" : 'Avanzosc S.L. (Urtzi)',
    "description": """
	This module modifies the purchase workflow in order to validate purchases that exceeds minimum amount set by configuration wizards. \
	With this module, you will be able to validate twice after the confirmation.
    """,
    'website': 'http://www.avanzosc.com',
    'init_xml': [],
    'update_xml': [
       'security/purchase_triple_validation_security.xml',
	   'purchase_triple_validation_workflow.xml',
	   'purchase_triple_validation_installer.xml',
       'purchase_triple_validation_view.xml',
	    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate' : '',

}
