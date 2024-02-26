# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Line Update Seller",
    "version": "12.0.1.1.0",
    "category": "Purchases",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["product", "purchase", "purchase_order_line_input"],
    "excludes": [],
    "data": [
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
    ],
    "installable": True,
}
