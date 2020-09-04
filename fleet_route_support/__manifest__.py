# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Fleet Route Support",
    "version": "12.0.1.1.0",
    "depends": [
        "base",
        "fleet",
        "hr",
        "resource",
        "fleet_route_school",
    ],
    "author":  "AvanzOSC",
    "license": "AGPL-3",
    "website": "http://www.avanzosc.es",
    "data": [
        "views/fleet_route_support_view.xml",
        "views/res_partner_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
