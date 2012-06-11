# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "MRP Dimensions",
    "version" : "1.4",
    "author" : "Ting, AvanzOSC",
    'category': 'Generic Modules/Production',
    "license" : "GPL-3",
    "depends" : ["base","sale","mrp","stock","product", "mrp_jit"],
    "init_xml" : [],
    "description": """MRP dimensions:

Adds these dimensional variables (measurements) to products, production lot, production product line and purchase order line objects:
  * Shape (quadrangular, cylindrical,other)
  * Width
  * Length
  * Thickness
  * Density
  * Diameter
  * Purchase price in weight or in units
""",
    'update_xml': ["wizard/config_mrp.xml",
                   "mrp_dimensions_view.xml",
                   "purchase_wizard.xml",
                   "mrp_dimensions_data.xml",
                   "mrp_maker.xml",
                   ],
    'installable': True,
    'active': False,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
