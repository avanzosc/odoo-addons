# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Helpdesk Ticket With Task",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Operations/Helpdesk",
    "depends": [
        "helpdesk_sale",
        "sale_timesheet",
        "project",
    ],
    "data": [
        "views/helpdesk_tickect_view.xml",
        "views/project_task_view.xml",
    ],
    "installable": True,
}
