# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Batch Package Invoice Report",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "sale_order_package_usability",
        "stock_picking_invoice_link",
        "stock_picking_batch",
        "stock_move_line_package_dimension",
        "stock_picking_batch_package",
        "stock_picking_package_usability",
        "stock_picking_batch_invoice_rel",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_picking_batch_package_invoice_report.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_batch_views.xml",
        "views/stock_picking_views.xml",
        "report/stock_picking_batch_report.xml",
    ],
    "installable": True,
}
