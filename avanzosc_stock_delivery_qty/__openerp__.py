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
    "name": "Avanzosc Delivery Picking Quantity",
    "version": "1.0",
    "depends": ["stock", "purchase", "sale", "stock_supplier_packref", "account", "delivery"],
    "author": "Avanzosc S.L. (Ainara & Urtzi & Dani)",
    "category": "Custom Module",
    "description": """
    This module provide :
    * New field to specify quantity given by the supplier in order to invoice that quantity and take into account the other quantity in stock.
    """,
    "init_xml": [],
    'update_xml': [
                   "wizard/split_lot_wizard_view.xml",
                   "stock_picking_view.xml",
                   "weigth_delete_view.xml",
                   "wizard/change_move_data.xml",
                   "inventory_line_view.xml"
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}