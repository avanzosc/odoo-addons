# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Product Stock On Hand',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'AvanzOSC',
    'website': 'http://www.avanzosc.es',
    'contributors': [
        'Ainara Galdona <ainaragaldona@avanzosc.es>',
        'Ana Juaristi <anajuaristi@avanzosc.es>',
    ],
    'category': 'Warehouse Management',
    'depends': [
        'stock',
        ],
    'data': [
        'views/product_view.xml',
        'views/stock_location_view.xml',
        ],
    'post_init_hook': 'update_stock_on_hand_locations',
    'installable': True
}
