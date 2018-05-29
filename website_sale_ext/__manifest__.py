# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# Copyright 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'eCommerce - AvanzOsc extension',
    'category': 'Website',
    'summary': 'Sell Your Products Online',
    'version': '11.0.1.0.0',
    'author': "AvanzOSC",
    'license': "AGPL-3",
    'depends': ['product', 'website_sale'],
    'data': [
        'views/website_sale_backend_ext.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
