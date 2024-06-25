# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice Event Report Ticketbai",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons.git",
    "category": "Custom",
    "license": "AGPL-3",
    "depends": [
        "account_invoice_event_report",
        "l10n_es_ticketbai",
    ],
    "data": ["report/account_invoice_report.xml"],
    "installable": True,
    "auto_install": True,
}
