# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Multicompany email template',
    'version': '12.0.1.0.0',
    'depends': [
        "education_center_mail_template",
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/mail_template_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}
