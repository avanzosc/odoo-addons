# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Code Generator",
    "summary": "Auto-generate the product reference from brand, family, "
    "subfamily and season",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product_brand",
        "product_category_code",
        "product_simple_seasonality",
        "product_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_brand_views.xml",
        "views/seasonality_views.xml",
        "views/product_code_views.xml",
        "views/product_template_views.xml",
        "views/res_company_views.xml",
        "views/product_import_line_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
}
