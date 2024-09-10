{
    "name": "Account Move Date Grouping ",
    "version": "14.0.1.0.0",
    "summary": "Add Month, Year, and Quarter fields to invoices "
    "and related them to invoice lines for grouping.",
    "category": "Accounting",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_invoice_line_report",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
