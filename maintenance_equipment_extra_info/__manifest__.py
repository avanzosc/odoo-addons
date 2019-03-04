# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Maintenance Equipment Extra Info',
    'version': '11.0.1.0.0',
    'license': "AGPL-3",
    'summary': '''Equipment with extra info''',
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'category': 'Human Resources',
    'depends': [
        'maintenance',
        'account',
        'stock'
    ],
    'data': [
        "views/maintenance_equipment_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
