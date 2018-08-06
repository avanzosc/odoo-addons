# -*- coding: utf-8 -*-
# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice Automatic Pay Email",
    'version': '8.0.1.0.1',
    'license': "AGPL-3",
    'author': "AvanzOSC",
    'website': "http://www.avanzosc.es",
    'contributors': [
        "Gotzon Imaz <gotzonimaz@avanzosc.es>",
    ],
    "category": "Accounting & Finance",
    "depends": [
        'account',
    ],
    "data": [
        'data/account_invoice_automatic_pay_email_data.xml',
        'views/account_invoice_view.xml',
    ],
    "installable": True,
    "post_init_hook": "update_reminder_date",
}
