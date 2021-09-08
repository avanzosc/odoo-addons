# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Website Portal ZIP Autocomplete",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    'category': 'website',
    'version': '14.0.1.0.0',
    'depends': ['website_sale', 'base_location', 'website_bootstrap_select'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
    ]
}
