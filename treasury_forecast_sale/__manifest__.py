# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Treasury Forecast Sale",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Add project sale commitments to treasury forecasts",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "treasury_forecast_project",
        "sale_project",
    ],
    "data": [
        "views/treasury_forecast_sale_report_views.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
}
