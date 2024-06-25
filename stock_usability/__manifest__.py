# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Usability",
    "version": "14.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
        "purchase_stock",
        "product_usability",
        "product_supplierinfo_usability",
    ],
    "data": [
        "views/stock_warehouse_orderpoint_views.xml",
    ],
    "installable": True,
}
