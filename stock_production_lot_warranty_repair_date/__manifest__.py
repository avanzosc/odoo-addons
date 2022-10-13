# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Production Lot Warranty Repair Date",
    'version': '14.0.1.0.0',
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "repair",
        "stock_production_lot_warranty_date"
    ],
    "data": [
        "views/product_product_views.xml",
        "views/repair_order_views.xml",
        "views/stock_production_lot_views.xml",
    ],
    "installable": True,
}
