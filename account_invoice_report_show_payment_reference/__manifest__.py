# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Report Show Payment Reference",
    "version": "14.0.1.0.0",
    "category": "Banking addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account",
        "account_payment_partner",
        "account_payment_mode",
    ],
    "data": [
        "report/account_move_report.xml",
        "views/account_payment_mode_view.xml",
    ],
    "installable": True,
}
