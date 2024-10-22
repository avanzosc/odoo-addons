{
    "name": "Account Move Product Manufacturer Pivot",
    "version": "14.0.1.0.0",
    "summary": "Adds product category and manufacturer fields "
    "to invoice and sale order lines pivot views.",
    "category": "Accounting",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "account",
        "sale",
        "product_manufacturer",
        "mrp_sale_info",
    ],
    "data": [
        "views/account_move_views.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
}
