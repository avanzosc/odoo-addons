# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Website Event Type Custom",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    'category': 'website',
    'version': '14.0.1.0.0',
    'depends': [
        'event',
        'website_event_require_login',
        'event_registration_create_student'],
    'data': [
        'views/templates.xml',
        'views/views.xml',
    ]
}
