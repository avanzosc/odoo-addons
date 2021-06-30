# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Plane Number",
    "version": "14.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "product",
        "sale",
        "purchase"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_plane_number_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
