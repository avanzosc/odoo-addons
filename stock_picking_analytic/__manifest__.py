# Copyright 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Analytic Accounting for Stock Inventory",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "summary": """Stock picking with analytic account""",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Accounting/Accounting",
    "depends": [
        "analytic",
        "stock",
        "stock_account",
    ],
    "data": [
        "views/stock_picking_view.xml",
        "views/account_analytic_account_view.xml",
        "views/account_analytic_line_view.xml",
    ],
    "installable": True,
}
