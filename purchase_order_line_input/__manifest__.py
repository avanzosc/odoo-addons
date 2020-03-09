# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Purchase Order Line Input',
    'summary': 'Search, create or modify directly purchase order lines',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'Tecnativa, Avanzosc, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order_line_view.xml',
    ],
}
