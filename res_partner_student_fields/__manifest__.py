# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Res partner student fields',
    'version': '12.0.1.0.0',
    'depends': [
        "base",
        "education",
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Res partner student fields''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/res_partner_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}
