# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Lot Dimension Purchase",
    "version": "18.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase_stock",
        "stock_lot_dimension",
    ],
    "data": [
        "views/product_supplierinfo_view.xml",
        "views/purchase_order_view.xml",
        "views/stock_lot_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_quant_view.xml",
    ],
    "installable": True,
}
