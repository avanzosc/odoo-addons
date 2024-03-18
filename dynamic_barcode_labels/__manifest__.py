# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

{
    'name': 'Print Dynamic Barcode Labels (Product/Template/Purchase/Picking)',
    "version": "8.0",
    'author': 'TidyWay',
    'category': 'product',
    'website': 'http://www.tidyway.in',
    'summary': 'Print Labels from Product / Product Templates / Quotation / Purchase / Picking',
    'description': '''Print Dynamic Barcode Labels''',
    'depends': ['stock', 'web', 'purchase'],
    'data': [
             'data/barcode_config.xml',
             'security/barcode_label_security.xml',
             'security/ir.model.access.csv',
             'wizard/barcode_labels.xml',
             'views/barcode_config_view.xml',
             'views/barcode_labels_report.xml',
             'views/barcode_labels.xml',
             'views/menu_view.xml'
             ],
    'price': 50,
    'currency': 'EUR',
    'installable': True,
    'license': 'OPL-1',
    'application': True,
    'auto_install': False,
    'images': ['images/label.jpg'],
    'live_test_url': 'https://youtu.be/SPQZ8p7ATN4'
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
