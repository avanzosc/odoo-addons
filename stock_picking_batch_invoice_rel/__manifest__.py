# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Batch Invoice Rel",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "depends": ["account", "stock_picking_batch", "stock_picking_invoice_link"],
    "data": [
        "views/account_move_views.xml",
        "views/stock_picking_batch_views.xml",
    ],
    "installable": True,
}
