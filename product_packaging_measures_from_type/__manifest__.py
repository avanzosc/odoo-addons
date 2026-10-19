# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Packaging Measures From Type",
    "summary": "Calculate product packaging weight and height from package "
    "types and detect pallets",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "depends": [
        "product_packaging_is_pallet",
        "product_packaging_dimension",
    ],
    "data": [
        "views/stock_package_type_views.xml",
        "data/ir_actions_server_data.xml",
    ],
    "installable": True,
    "application": False,
}
