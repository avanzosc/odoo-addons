# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': "Default Package for Product Category",
    'summary': """
        Add default package type depending on the product category. 
        """,
    "author": "AvanzOSC",
    'website': 'http://www.avanzosc.es/',
    'version': '1.0',
    'depends': ['product', 'stock', 'stock_picking_sorted'],
    'data': [
        'views/product_category_view.xml',
        "views/product_packaging_view.xml",
        'views/stock_picking_view.xml',
    ],
    'installable': True,
}
