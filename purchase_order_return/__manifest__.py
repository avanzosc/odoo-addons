# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Return",
    "summary": "Allow specifying return quantities directly on purchase order lines",
    "version": "18.0.1.0.0",
    "author": "AvanzOSC",
    "category": "Purchase Management",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase_order_confirm_usability",
        "purchase_sale_inter_company",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
