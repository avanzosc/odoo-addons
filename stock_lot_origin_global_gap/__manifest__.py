# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Lot Origin Global Gap",
    "version": "16.0.1.2.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "https://github.com/avanzosc/odoo-addons",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["stock", "mrp"],
    "data": [
        "views/product_template_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_lot_views.xml",
        "report/report_deliveryslip.xml",
        "report/report_package_barcode.xml",
        "report/report_stockpicking_operations.xml",
    ],
    "installable": True,
}
