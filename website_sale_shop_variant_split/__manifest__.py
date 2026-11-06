# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Sale Shop Variant Split",
    "summary": "Show each chosen attribute value of a product as a "
    "separate product in the online shop",
    "version": "18.0.1.0.0",
    "category": "Website/Website",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "website_sale",
    ],
    "data": [
        "views/product_attribute_views.xml",
        "views/product_template_views.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
