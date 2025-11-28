# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Mrp Package Procurement Sequence",
    "summary": "In MRP create package by sequence in procurement group.",
    "version": "16.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["mrp", "stock_move_line_divide"],
    "data": ["views/mrp_production_view.xml"],
    "installable": True,
}
