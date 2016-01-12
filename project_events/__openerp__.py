# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Meetings in Projects",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "Avanzosc, S.L.",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Event Management",
    "depends": [
        "project",
        "event",
    ],
    "data": [
        "data/event_data.xml",
        "views/event_view.xml",
        "views/project_view.xml",
        "wizard/create_meeting_from_task_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
