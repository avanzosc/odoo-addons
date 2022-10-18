# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Create Repair",
    'version': '14.0.1.2.0',
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "sale",
        "sales_team",
        "purchase",
        "stock",
        "repair",
        "sale_order_type",
        "account_move_line_sale_info"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_picking_create_repair_data.xml",
        "views/product_template_views.xml",
        "views/purchase_order_views.xml",
        "views/repair_order_views.xml",
        "views/sale_order_type_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/account_move_views.xml",
        "reports/invoice_report.xml",
        "reports/sale_order_report.xml"
    ],
    "installable": True,
}
