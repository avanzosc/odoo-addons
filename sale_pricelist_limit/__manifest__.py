# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Pricelist Limit',
    'version': '11.0.1.0.0',
    'depends': [
        'base', 'sale',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Sale Pricelist Limit''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/product_pricelist_view.xml',
        'views/sale_view.xml',
        ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
