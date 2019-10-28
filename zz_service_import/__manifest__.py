# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ZZ service import',
    'version': '12.0.1.0.0',
    'depends': [
        'contacts',
    ],
    'external_dependencies': {
        'python': [
            'xlrd',
        ],
    },
    'author':  "AvanzoSC",
    'license': "AGPL-3",
    'summary': '''ZZ Service Import''',
    'website': 'http://www.avanzosc.es',
    'data': [
      'security/ir.model.access.csv',
      'views/zz_service_import_view.xml',
    ],
    'installable': True,
}
