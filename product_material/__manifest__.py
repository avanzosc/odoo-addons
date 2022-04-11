# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Material",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Product",
    "depends": [
        "stock",
        "mrp"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_material_views.xml",
        "views/mrp_bom_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
