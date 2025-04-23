# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Order picking tree",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "product_brand",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "data": [
        "views/stock_picking_view.xml",
        "report/report_stock_picking_operations.xml",
    ],
    "installable": True,
}
