# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Analytic Line Project",
    "version": "16.0.1.0.0",
    "category": "Services/Timesheets",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "analytic",
        "analytic_usability",
        "hr_timesheet",
        "project_type",
        "sale_project",
    ],
    "data": ["views/account_analytic_line_views.xml"],
    "installable": True,
    "auto_install": False,
}
