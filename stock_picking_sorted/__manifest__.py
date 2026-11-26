# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Sorted",
    "version": "18.0.1.0.0",
    "summary": """Sort stock picking operations by product category
    and brand for improved organization in delivery and receipt views.""",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "product_brand",
        "stock_delivery",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "data": [
        "views/stock_picking_view.xml",
        "views/stock_move_view.xml",
        "report/report_stock_picking_operations.xml",
    ],
    "installable": True,
    "application": False,
}
