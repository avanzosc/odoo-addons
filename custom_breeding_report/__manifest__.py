# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Breeding Report",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_picking_batch_breeding",
        "stock_picking_batch_liquidation",
    ],
    "data": [
        "views/lineage_percentage_view.xml",
        "views/mother_lineage_relation_view.xml",
        "report/mother_lineage_relation_report_xlsx.xml",
        "report/lineage_percentage_report_xlsx.xml",
        "report/stock_picking_batch_report_xlsx.xml",
        "report/breeding_general_summary_xlsx.xml",
    ],
    "installable": True,
}
