# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Cmr Report",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "contacts"
    ],
    "data": [
        "report/stock_picking_cmr_report.xml",
        "views/stock_picking_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
