# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Event Sudent History",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "account_banking_mandate_usability",
        "event",
        "partner_contact_birthdate",
        "partner_contact_type",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Custom",
    "data": [
        "security/ir.model.access.csv",
        "views/event_student_history_view.xml",
    ],
    "installable": True,
}
