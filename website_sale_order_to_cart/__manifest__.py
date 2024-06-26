# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Sale Order to Cart Button",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "summary": """Add a button to move the sale order to the cart
                  and another button to set it to Sent state from the website cart""",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["sale", "website_sale"],
    "data": [
        "views/website_templates.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
