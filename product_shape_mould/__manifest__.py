# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Shape Mould",
    "version": "18.0.1.1.0",
    "category": "Manufacturing/Manufacturing",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "mrp",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_mould_views.xml",
        "views/product_template_views.xml",
        "views/stock_lot_views.xml",
        "views/product_shape_views.xml",
    ],
    "installable": True,
}
