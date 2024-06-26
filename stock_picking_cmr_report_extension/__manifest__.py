# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking CMR Report Extension",
    'version': '14.0.1.1.0',
    "author": "Avanzosc",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "contacts",
        "fleet",
        "stock_picking_cmr_report",
    ],
    "data": [
        "views/stock_picking_views.xml",
        "views/res_partner_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
