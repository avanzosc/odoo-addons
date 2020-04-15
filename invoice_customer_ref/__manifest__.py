# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Invoice Customer Ref',
    'version': '12.0.1.0.0',
    'depends': [
        'sale',
        'stock',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Invoice Customer Reference''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/invoice_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}
