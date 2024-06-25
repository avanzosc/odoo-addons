# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Production Lot Product Class",
    "version": "14.0.1.1.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "purchase",
        "sale",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_class_views.xml",
        "views/stock_production_lot_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/stock_production_lot_type_application_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
