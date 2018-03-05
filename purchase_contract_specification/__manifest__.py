# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Contract Specification',
    'version': '11.0.1.0.1',
    'category': 'Purchases',
    'author': 'AvanzOsc',
    'license': 'AGPL-3',
    'summary': 'Define conditions and specifications in purchase orders',
    'depends': [
        'purchase',
        'contract_specification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_condition_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_contract_specification_menu.xml',
        'views/purchase_portal_templates.xml',
    ],
    'installable': True,
}
