# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
#    Date: 01/07/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "AvanzOSC - tree_grid extension",
    "version": "1.0",
    "depends": ["tree_grid","sale","purchase","stock","account","avanzosc_calculate_coeficient_udv_automatically"],
    "author": "AvanzOSC S.L.",
    "category": "Generic",
    "description": """
    Este módulo añade la unidad de venta, y cantidad de venta editables en los tree de
    líneas de pedido de compra, y de venta, líneas de factura, y líneas de albaranes.
    """,
    "init_xml": [],
    'update_xml': ['sale_order_view_ext.xml',
                   'purchase_order_view_ext.xml',
                   'stock_picking_view_ext.xml',
                   'account_invoice_view_ext.xml',
                   'product_product_view_ext.xml'
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}