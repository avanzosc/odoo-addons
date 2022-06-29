# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Descarga",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "custom_saca_intercompany",
        "hr_timesheet_activity_begin_end",
        "stock_picking_batch",
        "stock_move_line_force_done",
        "mrp",
        "mrp_production_deconstruction"
    ],
    "data": [
        "data/saca_line_stage.xml",
        "data/partner_category.xml",
        "data/project.xml",
        "views/stock_move_line_view.xml",
        "views/saca_line_view.xml",
        "views/account_analytic_line_view.xml",
        "views/project_task_view.xml",
        "views/mrp_production_view.xml",
    ],
    "installable": True,
}
