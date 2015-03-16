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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Sale Invoice Group",
    "version": "1.0",
    "depends": [
        "stock_invoicing_type",
    ],
    "author": "OdooMRP team",
    "website": "www.odoomrp.com",
    "category": "Accounting & Finance",
    "description": """
This module allows to assign an invoicing group to each partner in which you
define a stand-by period between the delivery order and the invoicing. You
won't be able then of invoicing pickings of that partner if the period is not
due.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/account_invoice_group_view.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
