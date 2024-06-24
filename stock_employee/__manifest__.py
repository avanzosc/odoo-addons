# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Assign Employee to Stock Picking and Quant Package",
    "version": "14.0.1.0.0",
    "category": "Inventory",
    "summary": "Assign employees to stock picking and quant packages",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "license": "AGPL-3",
    "depends": ["stock", "hr"],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_quant_package_views.xml"
    ],
    "installable": True,
    "application": False,
}
