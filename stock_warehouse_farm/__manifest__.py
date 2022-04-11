# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Warehouse Farm Data",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
        "base_geolocalize",
        "contacts",
        "stock_production_lot_mother",
        "stock_picking_batch_breeding"
    ],
    "data": [
        "views/stock_warehouse_view.xml",
        "views/res_partner_view.xml",
        "views/stock_picking_batch_view.xml"
    ],
    "installable": True,
}
