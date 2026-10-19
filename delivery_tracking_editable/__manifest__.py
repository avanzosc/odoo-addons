# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Delivery Tracking Editable",
    "summary": "Allows editing carrier and tracking number in validated stock pickings",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Delivery",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["delivery"],
    "data": [
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
