# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Treasury Forecast Purchase",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Add project purchase commitments to treasury forecasts",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["treasury_forecast_project", "purchase"],
    "data": [
        "views/purchase_order_line_views.xml",
        "views/treasury_forecast_purchase_report_views.xml",
    ],
    "installable": True,
}
