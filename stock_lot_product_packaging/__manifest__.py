# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Lot Product Packaging",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["product", "stock", "product_logistics_uom"],
    "data": [
        "views/stock_package_type_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/stock_lot_views.xml",
        "views/stock_quant_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
