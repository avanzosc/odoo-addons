# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Custom Portal",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "website",
    "version": "18.0.1.0.0",
    "depends": [
        "website",
        "portal",
        "sale",
        "purchase",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/views.xml",
        "views/menu_views.xml",
    ],
}
