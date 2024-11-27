# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Picking Generate Zero Lines",
    "version": "14.0.1.0.0",
    "category": "Analytic",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "purchase_stock",
        "picking_generate_zero_lines",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "installable": True,
}
