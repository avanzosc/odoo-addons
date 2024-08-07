# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice With Start End Date Period",
    "version": "16.0.1.3.0",
    "category": "Invoices & Payments",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["sale", "sale_timesheet", "account", "contract"],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
