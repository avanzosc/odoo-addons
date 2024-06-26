# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Search Customerinfo",
    "version": "14.0.1.0.0",
    "category": "Sales Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://avanzosc.es/",
    "depends": [
        "product",
        "sale",
        "product_search_supplierinfo",
        "product_supplierinfo_for_customer",
    ],
    "data": [
        "views/product_customerinfo_views.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
