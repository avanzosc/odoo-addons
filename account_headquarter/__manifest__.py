# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Headquarter",
    'version': '14.0.1.5.0',
    "category": "Invoices & Payments",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale_order_headquarter",
        "purchase_order_headquarter",
        "account"
    ],
    "data": [
        "security/account_headquarter_security.xml",
        "views/account_move_views.xml",
        "views/account_move_line_views.xml",
        "views/account_group_views.xml",
    ],
    'installable': True,
    'auto_install': True,
}
