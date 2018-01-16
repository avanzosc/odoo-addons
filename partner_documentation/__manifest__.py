# Copyright (c) 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Documentation',
    'version': '11.0.1.0.0',
    'depends': [
        'base',
        'contacts',
        'mail',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Parner documentation''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_document_tmpl_view.xml',
        'views/document_template_view.xml',
        'views/partner_document_view.xml',
        'views/partner_view.xml',
        ],
    'demo': [
        "demo/document_tmpl_demo.xml",
        "demo/partner_document_demo.xml",
    ],
    'installable': True,
    'auto_install': False,
}
