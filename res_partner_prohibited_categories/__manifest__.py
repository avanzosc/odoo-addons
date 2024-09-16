# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3 (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Res Partner Prohibited Categories",
    "version": "16.0.1.0.0",
    "category": "Tools",
    "summary": "Module to manage prohibited product categories for partners",
    "author": "Unai Beristain",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "res_partner_delivery_point",
        "website_sale",
    ],
    "data": [
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
