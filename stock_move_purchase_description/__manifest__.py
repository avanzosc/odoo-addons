# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Purchase Description",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "stock",
    ],
    "data": [
        "views/stock_picking_views.xml",
        "report/report_deliveryslip.xml",
    ],
    "installable": True,
}
