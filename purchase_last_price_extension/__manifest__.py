# Copyright 2022 Daniel Campos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Last Price Extension",
    "version": "12.0.1.0.0",
    "category": "Purchase",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "purchase_last_price_info",
        "purchase_order_line_input",
    ],
    "excludes": [],
    "data": [
        "views/purchase_order_line_view.xml",
    ],
    "installable": True,
}
