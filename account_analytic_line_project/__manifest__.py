# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Analytic Line Project",
    "version": "16.0.1.0.0",
    "category": "Services/Timesheets",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["hr_timesheet"],
    "data": [],
    "installable": True,
    "auto_install": False,
    "post_init_hook": "_post_install_put_project_in_analytic_lines",
}
