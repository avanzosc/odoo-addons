# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Create Repair",
    'version': '14.0.1.0.0',
    "category": "Sales/CRM",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "sale",
        "purchase",
        "stock",
        "repair"
    ],
    "data": [
        "views/purchase_order_views.xml",
        "views/repair_order_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
    ],
    'installable': True,
}
