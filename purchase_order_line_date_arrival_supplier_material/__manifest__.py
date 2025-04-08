# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Line Date Arrival Supplier Material",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "category": "Inventory/Purchase",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["purchase_stock"],
    "data": [
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_views.xml",
    ],
    "installable": True,
}
