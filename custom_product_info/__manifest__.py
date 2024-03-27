# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Product Info",
    "version": "12.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_color_view.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
}
