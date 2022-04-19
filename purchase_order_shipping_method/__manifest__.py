# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order Shipping Method",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "delivery",
        "delivery_carrier_partner",
        "stock",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/delivery_carrier_view.xml",
        "views/purchase_order_view.xml",
        "views/stock_picking_view.xml",
        "views/transport_carrier_lines_to_invoice_view.xml",
    ],
    "installable": True,
}
