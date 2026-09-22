# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Res Partner Required Fields",
    "version": "18.0.1.0.0",
    "category": "Sales/CRM",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
        "product",
        "partner_group_purchase",
        "commission_oca",
        "delivery",
        "account_payment_partner",
    ],
    "data": [
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
