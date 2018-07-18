# Copyright 2016 Esther Martin - AvanzOSC
# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Reports for events",
    "version": "11.0.1.1.0",
    "category": "Marketing",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "event",
        "website_event_track",
    ],
    "data": [
        "views/event_event_view.xml",
        "views/event_track_view.xml",
        "views/event_template.xml",
        "data/report_paperformat.xml",
    ],
    "installable": True,
}
