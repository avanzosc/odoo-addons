# -*- coding: utf-8 -*-
# Copyright (c) 2017  Ainara Galdona <ainaragaldona@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Utilities',
    'version': '11.0.1.0.0',
    'license': "AGPL-3",
    'summary': '''Account utilities''',
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
    ],
    'category': 'Accounting & Finance',
    'depends': [
        'account_cancel',
    ],
    'data': [
        "views/account_invoice_view.xml",
        "views/account_move_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
