{
    "name": "Product Product Category",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Add a product category field to products and copy it from the template.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": ["product"],
    "data": [
        "views/account_move_views.xml",
        "views/product_product_views.xml",
        "views/stock_move_views.xml",
        "views/stock_move_line_views.xml",
    ],
    "installable": True,
    "application": False,
    "post_init_hook": "post_init_hook",
}
