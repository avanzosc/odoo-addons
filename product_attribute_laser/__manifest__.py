# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Attribute Laser",
    "version": "16.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_material_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
    ],
    "installable": True,
}
