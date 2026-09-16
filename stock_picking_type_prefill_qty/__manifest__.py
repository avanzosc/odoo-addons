# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Type Prefill Quantity",
    "summary": "Let each operation type decide whether the quantity is "
    "auto-filled with the full demand when a move is reserved, or left "
    "at 0 to be entered manually",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_picking_type_views.xml",
    ],
    "installable": True,
}
