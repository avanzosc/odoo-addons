{
    "name": "Stock Replenishment Kits Quantity",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Shows kit quantity in stock replenishment.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "mrp",
        "sale_order_basket_number",
        "mrp_bom_component_menu",
    ],
    "data": [
        "views/mrp_bom_line_views.xml",
        "views/stock_replenishment_views.xml",
    ],
    "installable": True,
    "application": False,
}
