# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Penalties",
    "version": "14.0.1.0.0",
    "category": "Accounting",
    "summary": "Manage penalty invoicing",
    "depends": ["account", "sale", "product", "sales_team"],
    "data": [
        "security/ir.model.access.csv",
        "data/penalty_type_data.xml",
        "views/penalty_views.xml",
        "views/penalty_type_views.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
}
