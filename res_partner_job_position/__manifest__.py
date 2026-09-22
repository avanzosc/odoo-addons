# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Res Partner Job Position",
    "version": "18.0.1.0.0",
    "category": "Sales/CRM",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["account", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/res_partner_function_views.xml",
    ],
    "installable": True,
}
