# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order Shipping Method",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "delivery",
        "stock_delivery",
        "delivery_carrier_partner",
        "stock",
        "stock_picking_date_done",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/transport_carrier_lines_to_invoice_security.xml",
        "views/delivery_carrier_view.xml",
        "views/purchase_order_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_move_line_view.xml",
        "views/transport_carrier_lines_to_invoice_view.xml",
    ],
    "installable": True,
    # "pre_init_hook": "pre_init_hook",
}
