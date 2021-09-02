# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Event Registration Confirm Group",
    "version": "14.0.1.0.0",
    "category": "Marketing/Events",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "event_registration_action",
        "event_sale_registration_action"
    ],
    "data": [
        "security/event_registration_confirm_group.xml",
        "views/event_registration_views.xml",
        "wizard/wiz_event_reg_confirm_participant_sale_order_views.xml",
        "wizard/wiz_event_registration_confirm_participant_views.xml",
    ],
    "installable": True,
}
