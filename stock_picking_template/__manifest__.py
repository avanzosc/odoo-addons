# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Picking Template',
    'version': '12.0.1.0.0',
    'depends': [
        'stock',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Stock Picking Template''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/stock_picking_view.xml',
        'wizard/stock_picking_duplicate_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}
