# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Page Menu School',
    'version': '12.0.1.0.0',
    "category": "Education",
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'website': 'http://www.avanzosc.es',
    'depends': [
        "base",
        "education",
        'website'
    ],
    'data': [
        'views/website_page_view.xml',
        'views/website_menu_view.xml'
        ],
    'installable': True
}
