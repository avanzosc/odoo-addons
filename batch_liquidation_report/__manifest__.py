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
        "web",
        "stock_picking_batch_liquidation",
        "report_qweb_element_page_visibility",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ticket_paperformat.xml",
        "report/liquidation_account_move_report.xml",
        "report/liquidation_cost_report.xml",
        "report/fattening_cost_report.xml",
        "report/farmer_report.xml",
        "report/stock_picking_report.xml",
        "report/sale_order_report.xml",
        "report/purchase_order_report.xml",
        "report/account_move_report.xml",
        "report/stock_by_breeding_xlsx.xml",
        "views/stock_picking_batch_view.xml",
        "wizard/stock_by_breeding_wizard_view.xml",
    ],
    "installable": True,
}
