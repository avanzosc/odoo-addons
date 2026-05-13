# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Batch Report PA",
    "summary": "Picking batch report grouped by customer and date.",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "depends": [
        "stock_picking_batch",
        "stock_move_qty_by_packaging",
        "custom_mrp_line_cost",
    ],
    "data": [
        "report/report.xml",
    ],
    "installable": True,
}
