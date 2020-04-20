# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Education Group Mail List',
    'version': '12.0.1.0.0',
    'depends': [
        'education',
        'mass_mailing',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Education Group Mail List''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/mail_mass_mailing_list_view.xml',
        'views/education_group_student_progenitor_report_view.xml',
        "security/ir.model.access.csv",
        ],
    'installable': True,
    'auto_install': False,
}
