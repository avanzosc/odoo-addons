
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
    "name": "Sequence on sale_order_line",
    "version": "1.0",
    "depends": ["sale",
                "account",
                "stock"],
    "author": "AvanzOSC",
    "category": "CRM",
    "description": """
    This module provide : 
     -Add sequence for the module sale_order_line.
     -Add sequence for the module stock_move.(Stock_picking view).
     -Add sequence for the account_invoice_line.
    """,
    "init_xml": [],
    'update_xml': ["sale_order_line_add_seq_view.xml",
                   "account_invoice_line_add_seq.xml",
                   "stock_move_add_seq_view.xml"
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}