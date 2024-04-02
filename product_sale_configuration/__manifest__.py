# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Sale Configuration",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "stock",
        "stock_account",
        "purchase_last_price_info",
        "invoice_supplier_last_price_info",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "data": [
        "security/product_sale_configuration_data.xml",
        "security/ir.model.access.csv",
        "views/product_category_sale_price_view.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "wizard/wiz_change_product_temp_category_sale_price_view.xml",
        "wizard/wiz_change_product_temp_pvp_manual_view.xml",
        "wizard/wiz_recalculate_product_temp_sale_price_view.xml",
    ],
    "installable": True,
}
