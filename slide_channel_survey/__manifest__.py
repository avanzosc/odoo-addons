# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Slide Channel Survey",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    'category': 'website',
    'version': '14.0.1.1.0',
    'depends': ['survey', 'website_slides', 'slide_partner_menu'],
    'data': [
        #'security/ir.model.access.csv',
        'security/slide_channel_survey_security.xml',
        'report/evaluate_certification_report.xml',
        'views/views.xml',
        'views/menus.xml',
        'views/event_event_views.xml',
        'views/event_track_views.xml',
    ]
}
