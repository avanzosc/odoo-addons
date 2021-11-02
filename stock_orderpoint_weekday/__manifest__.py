# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Orderpoint Weekday",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "stock",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Warehouse Management",
    "data": [
        "security/ir.model.access.csv",
        "security/stock_security.xml",
        "views/stock_orderpoint_view.xml",
        "views/stock_orderpoint_weekdays_view.xml",
    ],
    "installable": True,
}
