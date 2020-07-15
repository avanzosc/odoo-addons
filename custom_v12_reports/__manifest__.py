# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Custom v12 Reports',
    'version': '12.0.1.0.0',
    'depends': [
        'portal',
        'website',
        'sale_management',
        'account',
        'account_banking_mandate',
        'sale_school',
        'education_center_mail_template'
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Custom v12 Reports''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'report/sale_order_report_view.xml',
        'report/sale_order_report_view2.xml',
        'report/sale_order_report_view3.xml',
        'report/sale_order_report_view4.xml',
        'report/sale_order_report_view5.xml',
        'report/account_banking_mandate_report_view.xml',
        'report/school_issue_report_view.xml',
        'report/school_issue_report_view2.xml',
        'report/report_button_view.xml',
        'report/report_header_view.xml',
        'report/sale_order_full_report_view.xml',
        'views/sale_order_website_templates.xml',
        'views/account_banking_mandate_website_templates.xml'
        ],
    'installable': True,
    'auto_install': False,
}
