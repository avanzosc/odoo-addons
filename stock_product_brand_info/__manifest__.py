# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock Product Brand Info",
    "version": "16.0.1.0.0",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "Avanzosc",
    "license": "AGPL-3",
    "depends": ["stock", "product_brand_supplierinfo"],
    "data": [
        "report/stock_picking_report.xml",
        "views/stock_move_line_views.xml",
        "views/stock_move_views.xml",
        "views/stock_quant_views.xml",
    ],
    "installable": True,
}
