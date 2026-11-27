# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking No Origin",
    "summary": "Filter to display pickings whose origin order does not exist.",
    "version": "18.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "license": "AGPL-3",
    "depends": ["sale", "purchase", "stock_picking_type_category"],
    "data": [
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
