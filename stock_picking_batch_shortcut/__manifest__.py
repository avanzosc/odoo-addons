# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Batch Shorcut",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "stock_picking_batch_extended",
    ],
    "data": ["views/stock_picking_batch_views.xml"],
    "installable": True,
    "auto_install": True,
}
