# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Product Attribute Hidden",
    "summary": "Hide attributes that do not create variants from the product "
    "configuration",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "sale",
    ],
    "data": [
        "views/product_attribute_views.xml",
    ],
    "uninstall_hook": "uninstall_hook",
    "installable": True,
}
