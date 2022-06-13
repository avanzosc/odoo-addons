# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Production Lot Fleet Vehicle",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales/CRM",
    "depends": [
        "fleet",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle_views.xml",
        "views/stock_production_lot_views.xml",
        "views/fleet_vehicle_model_type_views.xml",
        "views/fleet_vehicle_model_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
