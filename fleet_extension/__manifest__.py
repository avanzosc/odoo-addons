# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Extension",
    'version': '14.0.4.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Sales/CRM",
    "depends": [
        "fleet",
        "product",
        "stock",
        "sale_management",
        "stock_production_lot_fleet_vehicle"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle_model_views.xml",
        "views/fleet_vehicle_model_collection_views.xml",
        "views/fleet_vehicle_views.xml",
        "views/fleet_vehicle_model_type_views.xml",
        "views/stock_production_lot_views.xml",
        "views/product_template_views.xml",
        "views/fleet_vehicle_range_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
