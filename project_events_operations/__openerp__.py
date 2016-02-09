# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Project events operations",
    "version": "1.0",
    "depends": [
        "project_events"
    ],
    "author": "Avanzosc, S.L.",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
    ],
    "category": "Project Management",
    "description": """
    Copy project events to other project
    """,
    'data': [
        "wizard/copy_event_view.xml",
        "wizard/events_date_modify_view.xml",
        "wizard/event_timetable_unify_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
