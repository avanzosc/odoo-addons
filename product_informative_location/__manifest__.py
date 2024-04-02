# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Informative Location",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "stock",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Warehouse",
    "data": [
        "security/ir.model.access.csv",
        "views/product_informative_location_views.xml",
        "views/product_informative_location_precision1_views.xml",
        "views/product_informative_location_precision2_views.xml",
        "views/product_informative_location_precision3_views.xml",
        "views/product_product_views.xml",
        "views/stock_location_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_inventory_views.xml",
    ],
    "installable": True,
}
