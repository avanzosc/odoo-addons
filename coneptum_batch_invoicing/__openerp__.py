# -*- encoding: utf-8 -*-
##############################################################################
#
#    Coneptum - Toni Bagur toni.bagur@coneptum.com
#    Copyright (C) 2011 - 2012 Coneptum <www.coneptum.com>
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
    "name": "Coneptum Batch Invoicing",
    "version": "1.0",
    "depends": ["avanzosc_agreement_fixed_price"],
    "author": "Coneptum (Toni Bagur)",
    "category": "Custom Module",
    "description": """
        This module adds batch processing of agreements
    """,
    "init_xml": [],
    'update_xml': [
                   "ir_cron.xml"
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
