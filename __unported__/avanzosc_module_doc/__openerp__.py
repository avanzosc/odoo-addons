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
    "name": "AvanzOsc - Extended module documentation",
    "version": "1.0",
    "depends": ["base",
    ],
    "author": "Avanzosc - Alliance",
    "website": "http://www.avanzosc.es",
    "category": "Hidden",
    "description": """
    This module provide :
    """,
    "data": ["security/ir.model.access.csv",
             "data/extended_categories.xml",
             "data/areas.xml",
             "data/industries.xml",
             "module_documentation_view.xml",
             "module_documentation_images_view.xml",
             "module_view_ext.xml",
             "wizard/create_module_documentation_view.xml",
    ],
    "installable": True,
    "active": False,
}