# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Pricelist Item Discounts",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "product_pricelist_item_menu",
        "product_pricelist_import_hlc",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/pricelist_item_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
}
