# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Location Warehouse Change",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "stock",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Inventory",
    "summary": "Update the warehouse of a location and its children when the "
    "parent location changes.",
    "data": [
        "security/stock_location_warehouse_change_security.xml",
        "data/ir_actions_server_data.xml",
        "views/stock_location_views.xml",
    ],
    "installable": True,
}
