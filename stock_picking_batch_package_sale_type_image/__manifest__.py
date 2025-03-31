# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Package Sale Type Image",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_picking_batch_package",
        "sale_order_type_image",
    ],
    "data": ["data/layouts.xml", "views/stock_picking_batch_views.xml"],
    "installable": True,
}
