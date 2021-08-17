# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Registration Action",
    "version": '14.0.1.0.0',
    "author": "Avanzosc",
    "license": "AGPL-3",
    "category": "Marketing/Events",
    "depends": [
        "event",
    ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/wiz_event_registration_confirm_participant_views.xml',
        'wizard/wiz_event_registration_cancel_participant_views.xml',
        'wizard/wiz_event_registration_draft_participant_views.xml'
    ],
    "installable": True,
    "auto_install": True,
}
