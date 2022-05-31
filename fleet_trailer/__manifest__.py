# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Trailer",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales/CRM",
    "depends": [
        "stock_production_lot_fleet_vehicle",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle_classification_views.xml",
        "views/fleet_vehicle_variant_views.xml",
        "views/fleet_vehicle_version_views.xml",
        "views/fleet_vehicle_category_views.xml",
        "views/fleet_vehicle_mmta_views.xml",
        "views/fleet_vehicle_mma_views.xml",
        "views/fleet_vehicle_service_brake_type_views.xml",
        "views/fleet_vehicle_tire_dimension_views.xml",
        "views/fleet_vehicle_ic_iv_tire_views.xml",
        "views/fleet_vehicle_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
