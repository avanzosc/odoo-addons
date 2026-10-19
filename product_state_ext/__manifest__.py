# Copyright 2025 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product State Extension (Quants)",
    "version": "16.0.1.0.0",
    "category": "Inventory",
    "summary": "Show Product State on Inventory Quants with filters and group by.",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "product_state",
    ],
    "data": [
        "views/stock_quant_views.xml",
    ],
    "installable": True,
    "application": False,
}
