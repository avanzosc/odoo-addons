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
    "name": "MRP Product Configurator",
    "version": "1.0",
    "depends": ["mrp"],
    "author": "Avanzosc S.L. (Urtzi Odriozola)",
    "category": "Custom Modules",
    "description": """
    This module provide :
    Product configurator feature, which means you will be able to configure phantom BOMs \
    in order to choose corresponding component for each manufacturing order.
    """,
    "init_xml": [],
    'update_xml': [
                   "wizard/mrp_product_configurator_view.xml",
                   "res_partner/partner_view.xml",
                   "mrp_configurator_workflow.xml",
                   "mrp_production_view.xml",
                   "product_view.xml",
                   "sale_order_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}