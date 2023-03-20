# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Batch Valued",
    "version": "14.0.1.1.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "stock",
        "stock_picking_batch",
    ],
    "data": [
        "report/stock_picking_batch_valued_report.xml",
        "views/stock_move_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
