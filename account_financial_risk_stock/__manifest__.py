# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Financial Risk Stock",
    "version": "16.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["account_financial_risk", "stock"],
    "data": [
        "views/res_partner_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
