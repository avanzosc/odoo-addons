# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Technical Sheet Report",
    "version": "18.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product_brand",
        "product_category_default_profile",
        "product_simple_seasonality",
        "product_shape_mould",
    ],
    "data": [
        "views/product_brand_views.xml",
        "report/product_technical_sheet_report.xml",
        "report/product_technical_sheet_templates.xml",
    ],
    "installable": True,
}
