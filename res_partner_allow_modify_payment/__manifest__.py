# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Res Partner Allow Modify Payment",
    "version": "14.0.1.0.0",
    "category": "Invoices & Payments",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
        "account_payment_partner",
    ],
    "data": [
        "security/res_partner_allow_modify_payment_groups.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
