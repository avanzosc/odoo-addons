# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Default Address",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Set default invoice and delivery addresses per partner",
    "depends": ["base", "sale", "account"],
    "data": [
        "views/res_partner_views.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
}
