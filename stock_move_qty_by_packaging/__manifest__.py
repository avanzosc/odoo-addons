# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Qty By Packaging",
    "version": "16.0.1.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "sale_order_line_qty_by_packaging",
    ],
    "excludes": [],
    "data": [
        "views/stock_picking_views.xml",
        "report/deliveryslip_report.xml",
        "report/stockpicking_operations_report.xml",
    ],
    "installable": True,
}
