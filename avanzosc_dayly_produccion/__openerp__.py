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
    "name": "Avanzosc Dayly Produccion",
    "version": "1.0",
    "depends": ["avanzosc_estirpe"],
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "category": "Custom Module",
    "description": """
    This module provide :
    Módulo para granja de gallinas.
    Crea un nuevo objeto en la que se cargan la producción diaria por nave. Es un diario de producción.
    """,
    "init_xml": [],
    'update_xml': ["dayly_production.xml",
                   "wizard/wizard_calculate_production_journal_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}