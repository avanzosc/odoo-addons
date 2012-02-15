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
    "name": "Avanzosc Account Extension",
    "version" : "1.0",
    "description" : """ This module provides:
        Invoice: New wizard to unreconcile invoices account move.
        Account move line: On delete, also deletes the associated analytical lines.
        Account move: - When create lines, copies the previous line as before, without name and the account set as journals debit account.
                      - New button to apply moves changes into lines.
                      - New constraint to verify if the date is in the period specified.
        """,    
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "depends" : ["account_payment", "analytic"],
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["wizard/invoiced_unreconcile_view.xml",
                    "account_move.xml",
                    "account_invoice_view.xml"],
    "active" : False,
    "installable" : True  
}