# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Template Variant Create",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Sales",
    "depends": [
        "product",
        "sale_product_configurator",
    ],
    "data": [
        "views/product_views.xml",
        "wizards/create_product_variant_view.xml",
        "security/ir.model.access.csv",
    ],
    "license": "AGPL-3",
    'installable': True,
}
