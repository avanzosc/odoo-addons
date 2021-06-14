# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Extension",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Sales/CRM",
    "depends": [
        "fleet",
        "product",
        "stock"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle_model_views.xml",
        "views/fleet_vehicle_model_collection_views.xml",
        "views/fleet_vehicle_views.xml",
        "views/fleet_vehicle_model_type_views.xml",
        "views/stock_production_lot_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
