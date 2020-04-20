# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Education Group Report Mail List',
    'version': '12.0.1.0.0',
    'depends': [
        "base",
        "education",
        "education_group_mail_list",
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Education Group Report Mail List''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/education_group_report_mail_list_view.xml',
        'wizards/education_group_report_mail_list_wizard_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}
