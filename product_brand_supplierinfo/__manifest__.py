# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Product Brand Supplierinfo",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "Avanzosc",
    "license": "AGPL-3",
    "depends": ["product", "product_brand", "product_brand_purchase"],
    "data": [
        "security/product_brand_supplierinfo_groups.xml",
        "security/ir.model.access.csv",
        "views/product_brand_views.xml",
        "views/brand_product_footprint_views.xml",
        "views/brand_product_views.xml",
        "views/product_supplierinfo_views.xml",
        "views/product_template_views.xml",
        "wizard/wizard_dehomologation_reason_views.xml",
    ],
    "installable": True,
}
