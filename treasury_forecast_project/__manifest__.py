# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Treasury Forecast Project",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Manage and project future treasury movements",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["treasury_forecast", "project", "analytic_usability"],
    "data": [
        "security/ir.model.access.csv",
        "views/treasury_financing_views.xml",
        "views/treasury_forecast_views.xml",
        "views/treasury_forecast_project_report_views.xml",
        "views/project_project_views.xml",
        "views/account_analytic_account_views.xml",
    ],
    "installable": True,
}
