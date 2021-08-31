# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Extension",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Sales/CRM",
    "depends": [
        "fleet",
        "product",
        "stock",
        "sale_management"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle_model_views.xml",
        "views/fleet_vehicle_model_collection_views.xml",
        "views/fleet_vehicle_views.xml",
        "views/fleet_vehicle_model_type_views.xml",
        "views/stock_production_lot_views.xml",
        "views/product_template_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
