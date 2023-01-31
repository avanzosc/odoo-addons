# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Batch Liquidation Report",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock_picking_batch_liquidation",
    ],
    "data": [
        "report/liquidation_account_move_report.xml",
        "report/liquidation_cost_report.xml",
        "report/fattening_cost_report.xml"
    ],
    "installable": True,
}
