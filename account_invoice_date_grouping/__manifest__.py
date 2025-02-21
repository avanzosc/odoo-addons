# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Date Grouping",
    "version": "12.0.1.0.0",
    "summary": "Add Month, Year, and Quarter fields to invoices "
    "and related them to invoice lines for grouping.",
    "category": "Invoicing Management",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
