# Copyright 2022 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Final Position",
    "summary": "Some new fields added for Final Product variants",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons/",
    "category": "Inventory/Inventory",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_final_views.xml",
        "views/product_product_views.xml",
        "views/product_quartering_location_views.xml",
    ],
}
