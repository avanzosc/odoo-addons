# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2008 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Jordi Esteve <jesteve@zikzakmedia.com>
#						Daniel Campos <danielcampos@avanzosc.com>
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
	"name" : "OScommerce Interface / ZenCart",
	"version" : "1.0",
    "author" : "Axelor, Zikzakmedia, Avanzosc and NaN Projectes de Programari Lliure S.L.",
	"license" : "GPL-3",
	"category" : "Interfaces/CMS & eCommerce",
	"website" : "www.aulaerp.com/cursos-aulaerp/configuracion-y-funcionamiento-del-conector-openerp-oscommerce.html",
	"depends" : [
        "account_payment",
        "delivery",
        "nan_external_prices",
        "product",
        "sale",
        "stock",
    ],
	"description": """OSCommerce (Zencart) eCommerce interface synchronisation.

Syncro Oscommerce to Openerp
 1. Import/upgrade categories.
 2. Import/upgrade products. 
 3. Import Orders on selected status. On importing order, if not exists, customer is created automatically 

Syncro Openerp to Oscommerce
 1. Export products, prices, image, specials.
 2. Export Stocks. 
 3. Change Oscommerce Order status and include comments. Upload Osc Status and comments. 

Developed by Tiny, Axelor, Zikzakmedia and Ana Juaristi""",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : [
		"security/esale_oscom_security.xml",
		"security/ir.model.access.csv",
		"esale_oscom_view.xml",
		"esale_oscom_wizard.xml",
		"esale_oscom_product_view.xml",
		"shipping_product_data.xml"
	],
	"active": False,
	"installable": True
}
