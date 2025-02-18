# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Brand Supplier Relation",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Product",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "product_brand",
        "product_brand_supplierinfo",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_brand_views.xml",
        "views/res_partner_views.xml",
        "views/product_brand_supplier_relation_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_load_data_into_relational_table",
}
