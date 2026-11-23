# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Lot Dimension",
    "version": "18.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "product_dimension",
    ],
    "data": [
        "data/decimal_precision.xml",
        "views/stock_lot_view.xml",
        "views/stock_quant_view.xml",
        "views/product_view.xml",
        "views/product_category_view.xml",
    ],
    "installable": True,
}
