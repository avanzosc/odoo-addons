# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Sale Registration Action",
    "version": '14.0.1.0.0',
    "author": "Avanzosc",
    "license": "AGPL-3",
    "category": "Marketing/Events",
    "depends": [
        "event_sale",
    ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/wiz_event_registration_confirm_sale_order_views.xml',
        'wizard/wiz_event_reg_confirm_participant_sale_order_views.xml',
    ],
    
    "installable": True,
    "auto_install": True,
}
