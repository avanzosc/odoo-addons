# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Point of Sale Global Extra Discounts',
    'version': '8.0.0.1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'summary': 'Extra Global Discounts in the Point of Sale ',
    'author': 'AvanzOSC S.L.',
    'depends': ['pos_discount', 'point_of_sale'],
    'data': [
        'views/views.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'website': 'https://www.avanzosc.es/',
}
