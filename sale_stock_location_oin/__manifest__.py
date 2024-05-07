##############################################################################
#
# Copyright 2019 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    "name": "Sale Product By Location",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "summary": "Define a specific source location on each Sale Order Line",
    "author": "Odoo IT now",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "Other proprietary",
    "description": """
Sale Product By Location
========================
Allows to define a specific source location on each Sale Order line and sell the
products from the different locations, that may not be children of the default
location of the same SO picking type.
    """,
    "depends": [
        "base",
        "sale_management",
        "sale_stock",
        "sale_order_type",
        "sale_order_line_date",
    ],
    "data": [
        "views/sale_view.xml",
        "views/sale_order_type_view.xml",
        "views/stock_location_view.xml",
    ],
    "images": ["images/OdooITnow_screenshot.png"],
    "price": 15.0,
    "currency": "EUR",
    "installable": True,
    "application": False,
    "auto_install": False,
}
