{
    "name": "Account Invoice Margin",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Adds margin calculation fields to invoice lines and invoice totals.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "views/account_invoice_line_views.xml",
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "application": False,
}
