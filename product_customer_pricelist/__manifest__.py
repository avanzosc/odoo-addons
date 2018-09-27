# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Customer Pricelist',
    'version': '11.0.1.0.0',
    'depends': [
        'base', 'product', 'sale',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Product Customer Pricelist''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/product_view.xml',
        ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
