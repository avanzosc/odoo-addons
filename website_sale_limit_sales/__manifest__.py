# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Limit Website Sales',
    'category': 'Website',
    'sequence': 55,
    'summary': 'Define maximum quantity from brand/product that can be sold in website',
    "author": "AvanzOSC",
    "license": "AGPL-3",
    'website': 'http://www.avanzosc.es/',
    'version': '12.0.1.0.0',
    'depends': [
        'product',
        'product_brand',
        'sale',
        'website',
        'website_sale',
    ],
    'data': [
        'views/product_view.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
}
