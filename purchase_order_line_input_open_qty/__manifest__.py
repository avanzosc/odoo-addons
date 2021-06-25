# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase Order Line Input Open Qty",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Purchase",
    "depends": [
        "purchase_order_line_input",
        "purchase_open_qty",
    ],
    "data": [
        "views/purchase_order_line_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
