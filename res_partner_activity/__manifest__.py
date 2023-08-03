# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Res Partner Activity",
    "version": "14.0.1.0.0",
    "category": "Contacts",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contacts",
        "calendar",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/principal_activity_view.xml",
        "views/water_subactivity_view.xml",
        "views/industry_subactivity_view.xml",
        "views/calendar_event_view.xml",
    ],
    "installable": True,
}
