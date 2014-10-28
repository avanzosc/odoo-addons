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
    "name": "Project partner event registration",
    "version": "1.0",
    "depends": [
        "base",
        "project",
        "event",
        "project_events",
    ],
    "author": "OdooMRP team",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
    ],
    "website": "http://www.odoomrp.com",
    "category": "Project management",
    "description": """
Adds many partners to project and the possibility to add those partners
automatically to the events of the project
    """,
    "data": [
        "views/project_view.xml",
        "views/event_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
