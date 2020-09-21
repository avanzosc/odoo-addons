# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Invoice Student Field',
    'version': '12.0.1.0.0',
    "category": "Invoicing Management",
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'website': 'http://www.avanzosc.es',
    'depends': [
        "base",
        "account",
        'website'
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/account_invoice_website_templates.xml'
        ],
    'installable': True
}
