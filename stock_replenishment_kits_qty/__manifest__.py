{
    "name": "Stock Replenishment Kits Quantity",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Shows kit quantity in stock replenishment.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": ["stock", "mrp"],
    "data": [
        "views/stock_replenishment_views.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
}
