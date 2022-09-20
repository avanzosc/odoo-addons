# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Final Price By Pricelist",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "depends": [
        "product_final",
        "product_price_by_pricelist",
    ],

    "data": [
        "security/ir.model.access.csv",
        "views/product_final_price_by_pricelist_report_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
