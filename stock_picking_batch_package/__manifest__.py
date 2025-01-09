# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Package",
    "version": "16.0.1.1.0",
    "author": "AvanzOSC",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "delivery_carrier_partner",
        "stock_picking_batch",
        "stock_picking_package_usability",
    ],
    "data": [
        "views/stock_picking_batch_view.xml",
        "views/stock_picking_view.xml",
        "report/batch_report.xml",
        "report/picking_report_template.xml",
        "report/stock_picking_batch_by_package_report.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
