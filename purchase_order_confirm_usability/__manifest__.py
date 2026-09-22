# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Confirm Usability",
    "summary": "Button on purchase order to confirm and validate the picking",
    "version": "18.0.1.0.0",
    "category": "Purchase Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase_order_line_lot",
        "stock_picking_date_done",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "installable": True,
}
