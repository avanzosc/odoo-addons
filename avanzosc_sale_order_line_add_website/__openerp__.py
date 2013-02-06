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
    "name": "avanzosc_sale_order_line_add_website",
    "version": "1.0",
    "depends": ["base",
                "sale"],
    "author": "AvanzOSC",
    "category": "sale",
    "description": """
        Create website (wwww,description, traffic).
        Add website to sale order line.
        Create Account Analytic plan instace for those not previously exist.
        Create Account analytic account for those not previously exist.
        Asign 100% rate and 2 lines, product_name and website_name.
    """,
    "init_xml": [],
    'update_xml': ["avanzosc_sale_order_line_add_website_view.xml",
                   "company_father_add_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}