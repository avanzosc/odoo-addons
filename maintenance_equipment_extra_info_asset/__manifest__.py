# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Maintenance Equipment Extra Info Asset',
    'version': '11.0.1.0.0',
    'license': "AGPL-3",
    'summary': '''Equipment with purchase line asset''',
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'category': 'Accounting',
    'depends': [
        'maintenance_equipment_extra_info',
        'account_asset',
    ],
    'data': [
        "views/account_asset_asset_view.xml",
        "views/maintenance_equipment_view.xml",
        "views/account_invoice_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
