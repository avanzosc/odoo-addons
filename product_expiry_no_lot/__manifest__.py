# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Products Expiration Date (without trazability)",
    "version": "14.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "product",
        "product_expiry",
        "stock",
    ],
    "data": [
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
