# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Alternative Sale Code",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["product_sequence_by_category", "product_sale_configuration"],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "data": [
        "data/ir_sequence_data.xml",
        "views/product_product_view.xml",
        "wizard/wiz_generate_alternative_sale_code_view.xml",
    ],
    "installable": True,
}
