{
    "name": "Product Classification Fields",
    "version": "14.0.1.1.0",
    "category": "Product",
    "summary": "Adds classification fields to product template",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["product", "stock"],
    "data": [
        "views/product_template_views.xml",
        "views/product_series_view.xml",
        "views/product_model_view.xml",
        "views/product_application_view.xml",
        "views/product_family_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
}
