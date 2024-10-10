# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Package Usability",
    "version": "16.0.1.1.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_picking_batch",
        "stock_picking_package_usability",
        "stock_picking_batch_package",
    ],
    "data": [
        "views/stock_quant_package_view.xml",
        "views/stock_picking_batch_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
