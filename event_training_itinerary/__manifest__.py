# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Training Itinerary",
    "version": "14.0.1.1.0",
    "category": "Website/eLearning",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["website_slides", "event_slides", "slide_channel_technology"],
    "data": [
        "security/ir.model.access.csv",
        "data/event_training_itinerary_data.xml",
        "views/event_event_views.xml",
        "views/event_track_views.xml",
        "views/slide_channel_views.xml",
        "views/slide_channel_tag_views.xml",
        "views/slide_channel_tag_course_views.xml",
    ],
    "installable": True,
}
