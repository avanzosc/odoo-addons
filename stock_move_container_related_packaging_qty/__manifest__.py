# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Container Related Packaging Qty",
    "version": "14.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["sale", "stock", "sale_order_package_usability"],
    "data": [
        "views/sale_order_line_views.xml",
        "views/sale_order_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
