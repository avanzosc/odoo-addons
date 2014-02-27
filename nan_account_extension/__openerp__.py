# -*- encoding: latin-1 -*-
##############################################################################
#
# Copyright (c) 2010 NaN Projectes de Programari Lliure, S.L. All Rights Reserved.
#                    http://www.NaN-tic.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

{
    "name" : "NaN Account Extension",
    "version" : "1.0",
    "author" : "NaN·tic",
    "category" : "Accounting",
    "website": "http://www.nan-tic.com",
    "description": """\
This module adds some new features to account module, including:
- Automatic partner account creation, update and removal (Configurable per company).
- Avoids duplicate supplier invoices by checking no other invoice has the same partner, date and reference when the user tries to create the invoice.
- Allows searching draft account moves by adding the corresponding '*' before the ID.
- Ensures both Journal and Period are always consistent among account move and all its move lines. If the user changes Journal or Period in a move the change will be propagated to all lines and vice-versa.
- Makes 'date_due' field in invoices readonly when payment_term is set.
- Allows grouping invoice lines that have different products into the same account move line. (Configurable per journal).
- Allows ensuring new invoices do not have a date previous to the latest invoice in the journal, as required by the law of some countries such as Spain. (Configurable per journal).
- Ensures account moves created from bank statements use the sequence of the journal instead of keeping statement's numbering.
- Allows ensuring all moves of a given account have a partner associated with them.
""",
    "depends" : [
        'account',
	],
    "init_xml" : [],
    "update_xml" : [
        'account_view.xml',
        'company_view.xml',
        'partner_view.xml',
        'invoice_view.xml',
    ],
    "demo_xml" : [],
    "active": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
