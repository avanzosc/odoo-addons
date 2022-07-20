# Copyright (C) 2013 Obertix Free Software Solutions (<http://obertix.net>).
#                    cubells <info@obertix.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking Lots and Locations",
    "version": "12.0.2.0.0",
    "license": "AGPL-3",
    "category": "Tools",
    "author": "cubells",
    "website": "http://obertix.net",
    "depends": [
        "stock",
    ],
    "data": [
        # "wizard/serial_and_locations_view.xml",
        "wizard/import_lots_view.xml",
        "views/serial_lots_views.xml",
        "views/stock_production_lot_view.xml",
    ],
    "external_dependencies": {
        "python": [
            "xlrd",
        ],
    },
    "installable": True
}
