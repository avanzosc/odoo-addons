# Copyright 2019 Mentxu Isuskitza - AvanzOSC
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Fleet Route",
    "version": "12.0.8.0.0",
    "license": "AGPL-3",
    "depends": [
        "fleet",
        "hr",
        "resource",
        "partner_external_map",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Human Resources",
    "data": [
        "data/fleet_route_data.xml",
        "security/ir.model.access.csv",
        "security/fleet_route_security.xml",
        "views/fleet_route_view.xml",
        "views/fleet_route_name_view.xml",
        "views/fleet_route_stop_view.xml",
        "views/fleet_vehicle_view.xml",
        "views/res_partner_view.xml",
        "views/fleet_route_menu_view.xml",
    ],
    "installable": True,
}
