# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Page Require Login',
    'category': 'Website',
    'sequence': 55,
    "author": "AvanzOSC",
    "license": "AGPL-3",
    'website': 'http://www.avanzosc.es/',
    'version': '12.0.1.0.0',
    'depends': [
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/website_page_security.xml',
        'views/views.xml',
    ],
    'installable': True,
}
