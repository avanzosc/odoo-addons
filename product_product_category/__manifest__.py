{
    "name": "Product Product Category",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Add a product category field to products and copy it from the template.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": ["product"],
    "data": ["views/product_view.xml"],
    "installable": True,
    "application": False,
    "post_init_hook": "post_init_hook",
}
