# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Report",
    "version": "12.0.1.0.0",
    "category": "Warehouse",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale",
        "sale_stock",
        "stock",
        "purchase",
        "purchase_discount",
        "purchase_stock",
    ],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "reports/stock_report_view.xml",
    ],
    "installable": True,
}
