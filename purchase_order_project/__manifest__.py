# Copyright 2019 Alejandro Nieto - Okatent
# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase Order Project",
    "version": "18.0.1.0.0",
    "category": "Inventory/Purchase",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase",
        "hr_timesheet",
        "stock",
        "purchase_stock",
        "stock_picking_analytic",
    ],
    "data": ["views/purchase_order_views.xml", "views/stock_picking_views.xml"],
    "installable": True,
}
