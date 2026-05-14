# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Treasury Forecast",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Manage and project future treasury movements",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "base",
        "product",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/treasury_forecast_views.xml",
        "views/treasury_forecast_generate_lines_views.xml",
        "views/treasury_forecast_menu.xml",
        "views/treasury_financing_category_views.xml",
        "views/treasury_financing_views.xml",
        "views/account_move_views.xml",
        "views/account_move_line_views.xml",
        "data/treasury_financing_category_data.xml",
    ],
    "post_init_hook": "create_treasury_forecast_view",
    "installable": True,
    "application": False,
    "auto_install": False,
}
