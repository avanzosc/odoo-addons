# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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
    "name": "Sale Taxes Apportionment",
    "version": "1.0",
    "depends": [
        "sale",
        "stock",
    ],
    "author": "AvanzOSC",
    "category": "Custom Module",
    "website": "http://www.avanzosc.es",
    "description": """
    This module breaks down sale taxes in sale.order and stock.picking
    """,
    "data": [
        "security/apportionment_taxes.xml",
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "views/tax_apportionment_view.xml"
    ],
    "installable": True,
}
