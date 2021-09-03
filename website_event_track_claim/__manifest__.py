# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Event Track Claim",
    "version": '14.0.1.1.0',
    "author": "Avanzosc",
    "license": "AGPL-3",
    "category": "Marketing/Events",
    "depends": [
        "crm_claim",
        "website_event_track",
        "event_registration_student"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/event_track_views.xml',
        'views/crm_claim_views.xml',
        'views/event_event_views.xml',
        'wizard/wiz_event_participant_create_claim_views.xml'
    ],
    "installable": True,
}
