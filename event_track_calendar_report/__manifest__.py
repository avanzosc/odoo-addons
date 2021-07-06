# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Event track calendar report",
    "version": "14.0.1.0.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "calendar",
        "website_event_track"
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/event_track_report_views.xml",
    ],
    "installable": True,
}
