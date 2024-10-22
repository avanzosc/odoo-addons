# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Type Partner",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["purchase_order_type", "purchase_stock"],
    "excludes": [],
    "data": [
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
