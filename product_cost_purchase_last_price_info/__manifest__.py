# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Cost Purchase Last Price Info",
    "version": "14.0.2.2.0",
    "category": "Purchase Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_account",
        "purchase_last_price_info",
        "product_cost_visible",
        "stock",
        "purchase_last_price_info_discount",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/stock_quant_views.xml",
        "views/stock_valuation_views.xml",
    ],
    "installable": True,
}
