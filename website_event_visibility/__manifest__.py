# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Event Website Visibility",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    'category': 'website',
    'version': '14.0.1.0.0',
    'depends': ['event', 'website_event'],
    'data': [
        'security/website_event_security.xml',
        'views/event_templates.xml',
        'views/event_views.xml',
    ],
}
