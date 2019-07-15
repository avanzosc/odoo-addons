# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product attribute code field",
    "version": "8.0.2.0.2",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Product Management",
    "data": [
        "views/product_attribute_view.xml",
    ],
    "installable": True,
    "pre_init_hook": "assign_product_attribute_code",
}
