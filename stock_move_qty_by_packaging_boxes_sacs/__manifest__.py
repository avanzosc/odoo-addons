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
        "stock_move_line_force_done",
        "product_packaging_palet",
        "stock_move_qty_by_packaging",
        "uom",
    ],
    "excludes": [],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_move_line_views.xml",
        "report/deliveryslip_report.xml",
        "report/stockpicking_operations_report.xml",
    ],
    "installable": True,
}
