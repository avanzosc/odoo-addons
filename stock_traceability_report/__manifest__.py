# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Traceability Report",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
    ],
    "data": [
        "data/ir_actions_report.xml",
        "reports/lot_traceability_report.xml",
        "reports/stock_views.xml",
        "views/stock_lot_views.xml",
    ],
    "installable": True,
}
