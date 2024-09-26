# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Contact Type Analytic Account",
    "version": "14.0.1.0.0",
    "category": "Accounting/Accounting",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["partner_contact_type", "sale", "analytic", "account", "contract"],
    "data": [
        "views/res_partner_type_views.xml",
        "views/account_move_views.xml",
        "views/sale_order_views.xml",
        "views/account_analytic_line_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
