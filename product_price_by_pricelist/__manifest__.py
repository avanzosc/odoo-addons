# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Price By Pricelist",
    "version": "12.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/scheduled_action.xml",
        "views/product_price_by_pricelist_view.xml",
        "views/product_product_view.xml",
    ],
    "installable": True,
}
