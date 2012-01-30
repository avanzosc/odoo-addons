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
    "name": "Invoice Second Journal",
    "version": "1.0",
    "depends": ["account_invoice_create"],
    "author": "Avanzosc S.L.",
    "category": "Custom Modules",
    "website": "http://www.avanzosc.com",
    "description": """
    This module provide :
        * Features to chose between two different journals for each invoice type.
    """,
    "init_xml": [],
    'update_xml': ["sec_journal_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}