# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking With Analytic Account - Purchase link",
    "summary": "Purchase info in analytic from pickings",
    "version": "12.0.1.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "purchase_stock",
        "stock_picking_analytic",
    ],
    "data": [
        "views/account_analytic_line_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
