# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Category Sale Price",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "product_sale_configuration",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "data": [
        "wizard/wiz_change_product_category_sale_price_view.xml",
        "wizard/wiz_change_product_pvp_manual_view.xml",
        "wizard/wiz_recalculate_product_sale_price_view.xml",
        "views/product_product_views.xml",
    ],
    "installable": True,
}
