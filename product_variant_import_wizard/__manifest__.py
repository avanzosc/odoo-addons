# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Variant Import Wizard",
    "version": "18.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
        "product",
        "product_brand",
        "product_category_default_profile",
        "product_shape_mould",
        "sale",
        "stock",
        "account",
        "purchase",
    ],
    "data": [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/product_variant_import_wizard_view.xml",
        "views/product_variant_import_wizard_line_view.xml",
    ],
    "installable": True,
}
