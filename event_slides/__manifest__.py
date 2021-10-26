# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Slides",
    'version': "14.0.1.4.0",
    "author": "AvanzOSC",
    "category": "Website/eLearning",
    "depends": [
        "event_registration_student",
        "website_slides",
        "event_attendee_birthdate",
        "website_event_track",
    ],
    "data": [
        "views/event_event_views.xml",
        "views/slide_channel_views.xml",
        "views/slide_channel_partner_views.xml",
        "views/event_track_views.xml"
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
}
