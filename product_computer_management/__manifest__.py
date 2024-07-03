# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Computer Management",
    "version": "14.0.1.1.0",
    "category": "Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "purchase",
        "product_manufacturer",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_production_lot_view.xml",
        "views/battery_model_view.xml",
        "views/gen_view.xml",
        "views/grade_view.xml",
        "views/keyboard_view.xml",
        "views/lot_component_view.xml",
        "views/processor_view.xml",
        "views/product_model_view.xml",
        "views/ram_type_view.xml",
        "views/ram_view.xml",
        "views/resolution_view.xml",
        "views/screen_size_view.xml",
        "views/software_license_key_view.xml",
        "views/speed_view.xml",
        "views/storage_size_view.xml",
        "views/storage_type_view.xml",
        "views/chassis_view.xml",
    ],
    "installable": True,
}
