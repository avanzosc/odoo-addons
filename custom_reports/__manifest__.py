{
    "name": "Custom Reports",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Inherits and customizes invoice, sale order, and delivery document templates.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": ["account", "purchase", "stock"],
    "data": [
        "views/custom_report_invoice.xml",
        "views/custom_report_purchaseorder.xml",
        "views/custom_report_delivery.xml",
    ],
    "installable": True,
    "application": False,
}
