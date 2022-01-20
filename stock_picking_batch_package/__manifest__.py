# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Package",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": [
        "delivery_carrier_partner",
        "stock_picking_batch",
        "stock_picking_package_usability",
    ],
    "data": [
        "views/stock_picking_batch_views.xml",
        "report/batch_report.xml",
        "report/picking_report_template.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
