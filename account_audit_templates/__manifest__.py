# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Audit Templates",
    "version": "14.0.1.0.0",
    "category": "Accounting",
    "summary": "Technical audit visibility for chart template models",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "views/template_views.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
}
