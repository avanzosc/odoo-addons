# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Create Repair Warranty",
    'version': '14.0.1.0.0',
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_picking_create_repair",
        "product_expiry"
    ],
    "data": [
        "views/product_product_views.xml",
        "views/repair_order_views.xml",
        "views/stock_production_lot_views.xml",
    ],
    "installable": True,
}
