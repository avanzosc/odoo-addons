
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
    "name": "Avanzosc Report Contract Extension",
    "version": "1.0",
    "depends": ["report_contract","avanzosc_purchase_order_restructure_view","purchase_requisition", "sale","hr_contract"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
        Avanzosc Custom Modules:
        
        This module creates two new object "Contract Particular Conditions" and "Contract General Conditions".
        These conditions of contract can be defined for Sale Orders, Purchase Orders, and in Employee Contracts.

    """,
    "init_xml": [],
    'update_xml': ['wizard/contract_select_template_purchase_view.xml',
                   'wizard/contract_select_template_sale_view.xml',
                   'wizard/contract_select_template_rrhh_view.xml',
                   'report_contract_template_master_line_view.xml',
                   'report_contract_template_view.xml',
                   'report_contract_template_line_view.xml',
                   'contract_conditions_ext_view.xml',
                   'purchase_order_ext_view.xml',
                   'sale_order_ext_view.xml',
                   'hr_contract_ext_view.xml'
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
