# -*- coding: utf-8 -*-
# Copyright (C) 2016-2019 Artem Shurshilov <shurshilov.a@yandex.ru>
# License LGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Widget image preview',
    'summary': """Adds functional preview (open/popup) image in original size 
    Enlarge image Enlarge images product images preview product images picture
    foto product photo product preview enlarge """,
    'description': """
This is extension for <field widget="image"> widget image
==============================================
* STOCK and CONTACT example:
    * open image on click in original size in popup
    * close on close button
    * close on click on/out image

""",
    'author': 'Shurshilov Artem',
#    "website": "https://vk.com/id20132180",
    'website': "http://www.eurodoo.com",
    
    # Categories can be used to filter modules in modules listing
    'category': "Tools",
    'version': '12.5.0.0',
    # any module necessary for this one to work correctly
    'depends': ['web','mail', 'swipe_images_backend'],
    "license": "LGPL-3",
#    'price': 9.99,
#    'currency': 'EUR',
    # always loaded
    'images':[
            'static/description/stock_open2.png',
            'static/description/stock_open.png',
            'static/description/stock_cursor.png',
    ],
    'data': [ 'views/form_image_preview_templates.xml', ],   
    'qweb': [ 'static/src/xml/image.xml', ],
    'installable': True,
    'application': False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    'auto_install': False,
}