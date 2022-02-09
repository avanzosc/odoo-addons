# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Move Time Type",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "https://www.avanzosc.es",
    "category": "Sales/CRM",
    "depends": [
        "sale_timesheet",
        "account_invoice_with_start_end_date_period",
        "event_track_cancel_reason"
    ],
    "data": [
        "views/account_move_line_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
