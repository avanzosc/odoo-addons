# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Weight Done",
    "summary": "Creates a checkbox for weight validation",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Manufacturing/",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "mrp",
    ],
    "data": [
        "views/mrp_production_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
