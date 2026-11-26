# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Res Partner Eori Number",
    "version": "18.0.1.0.0",
    "category": "Sales/CRM",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "contacts",
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/widget_contact_views.xml",
    ],
    "pre_init_hook": "remove_studio",
    "installable": True,
}
