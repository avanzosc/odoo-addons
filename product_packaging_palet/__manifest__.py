# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Packaging Palet",
    "version": "16.0.1.1.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "https://github.com/avanzosc/odoo-addons",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["product", "stock", "sale_order_line_qty_by_packaging"],
    "data": [
        "views/product_packaging_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
