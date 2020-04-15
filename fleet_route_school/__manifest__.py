# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Fleet Route School",
    "version": "12.0.2.0.0",
    "category": "Human Resources",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "fleet",
        "fleet_route",
        "contacts_school",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/fleet_route_school_data.xml",
        "views/fleet_route_stop_passenger_view.xml",
        "views/fleet_route_stop_view.xml",
        "views/fleet_route_view.xml",
        "views/fleet_vehicle_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
