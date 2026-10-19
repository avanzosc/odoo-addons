# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Create Repair Sale Subscription",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_picking_create_repair",
        "sale_subscription",
    ],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
