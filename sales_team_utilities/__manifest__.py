# Copyright 2018 Eider Oyarbide  <eideroyarbide@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sales Team Utilities',
    'version': '11.0.1.0.0',
    'category': 'Sales',
    'depends': [
        'sales_team',
        ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Sales Channels''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/res_partner_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}
