# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Order Quality Inspection",
    "summary": "Show quality inspections shortcut on sale orders",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "quality_control_mrp_oca",
        "quality_control_stock_oca",
        "mrp_sale_info",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "data": ["views/sale_order_views.xml"],
    "installable": True,
    "application": False,
}
