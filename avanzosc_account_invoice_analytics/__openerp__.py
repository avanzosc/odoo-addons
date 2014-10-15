# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
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
    "name": "AvanzOsc - Invoice from Analytics extension Supplier Invoices",
    "version": "1.0",
    "depends": ["account_invoice_analytics","project",
                "hr_timesheet_invoice"],
    "author": "AvanzOSC",
    "category": "Generic Modules/Accounting",
    "website": "http://www.avanzosc.es",
    "complexity": "normal",
    "description": """
    It allows creating supplier invoices from analytics
    """,
    "init_xml": ["data/account_analytic.xml"],
    "update_xml": ["wizard/hr_timesheet_invoice_create_view.xml",
                   "account_analytic_view.xml"],
    "demo_xml": [],
    "installable": True,
    "active": False,
#    "certificate": 'certificate',
}