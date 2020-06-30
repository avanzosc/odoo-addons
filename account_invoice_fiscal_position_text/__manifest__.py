# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Invoice Fiscal Position Text',
    'version': '12.0.1.0.0',
    "category": "Invoicing Management",
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'website': 'http://www.avanzosc.es',
    'depends': [
        "base",
        "account"
    ],
    'data': [
        'views/account_invoice_fiscal_position_text_view.xml',
        ],
    'installable': True
}
