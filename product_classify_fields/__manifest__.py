{
    "name": "Product Classification Fields",
    "version": "14.0.1.1.0",
    "category": "Product",
    "summary": "Adds classification fields to product template",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "product",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_series_view.xml",
        "views/product_model_view.xml",
        "views/product_application_view.xml",
        "views/product_family_view.xml",
    ],
    "installable": True,
}
