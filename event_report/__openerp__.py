# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Reports for events",
    "summary": "",
    "version": "8.0.1.0.0",
    "category": "Marketing",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "event",
        "report",
        "website_event_track",
    ],
    "data": [
        "views/event_track_view.xml",
        "views/event_template.xml",
        "data/report_paperformat.xml",
    ],
    "installable": True,
}
