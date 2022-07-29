# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking Project",
    "version": "14.0.1.0.0",
    "category": "Services/Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_picking_analytic",
        "project",
        "hr_timesheet",
    ],
    "data": [
        "views/project_task_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
