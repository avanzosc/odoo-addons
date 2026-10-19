# Copyright 2022 Patxi lersundi
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Final",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "license": "AGPL-3",
    "version": "16.0.1.0.0",
    "depends": [
        "stock",
        "product",
        "product_alternative_sale_code",
        "product_second_name",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_final_views.xml",
        "views/product_final_view_version_views.xml",
        "views/product_final_product_list_version_views.xml",
        "views/product_product_views.xml",
        "views/sale_product_location_exploded_views.xml",
        "wizard/wiz_duplicate_product_location_exploded_view.xml",
    ],
    "installable": True,
}
