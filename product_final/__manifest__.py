# Copyright 2022 Patxi lersundi 
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Final",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/mrp-addons",
    "category": "Sales",
    "license": "AGPL-3",
    "version": "12.0.1.1.0",
    "depends": ["stock",
                "product",
                ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_final_views.xml",
        "views/product_product_views.xml",
        "views/sale_product_location_exploded_views.xml",
        ],
    "installable": True,
}
