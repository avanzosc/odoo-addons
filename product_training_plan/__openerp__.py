# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Training Plan",
    "version": "8.0.2.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    "category": "Sales Management",
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/product_training_plan_data.xml",
        "views/product_product_view.xml",
        "views/training_plan_category_view.xml",
        "views/training_plan_view.xml",
        "views/product_training_plan_view.xml",
    ],
    "installable": True,
}
