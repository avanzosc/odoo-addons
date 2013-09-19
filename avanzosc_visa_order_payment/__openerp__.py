# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
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
    "name": "Avanzosc visa order payment",
    "version": "1.0",
    "depends": ["avanzosc_agreement_fixed_price"],
    "author": "AvanzOSC",
    "category": "Custom Module",
    "description": """
This module implements a new invoicing method for sale orders. It is complemented whit the invoicing method, from analytics. 
All orders marked with credit card payment, will be divided in two when they are invoiced, those lines corresponding to products payable with credit card will be in a individual invoice that will be marked has paid. The rest of lines will create analytics lines to be invoiced later.
    """,
    "init_xml": [],
    'update_xml': ['visa_payment_fields_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}