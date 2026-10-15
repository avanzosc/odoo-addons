# Copyright 2025 Eñaut Alberdi Korta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Public Category Product Count",
    "version": "18.0.1.0.2",
    "summary": """Displays the number of products
    per public category in the eCommerce backend""",
    "author": "AvanzOsc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Website/Website",
    "depends": ["website_sale"],
    "data": [
        "views/product_public_category_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}
