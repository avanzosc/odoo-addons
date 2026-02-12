{
    "name": "Product Fields Verify Prepare",
    "version": "14.0.1.0.0",
    "category": "Custom",
    "summary": "Custom module for Supertronic with additional fields",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "AvanzOSC",
    "depends": [
        "sale",
        "project",
        "sale_project",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/project_task_views.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}
