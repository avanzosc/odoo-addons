# -*- coding: utf-8 -*-
# (c) 2016 Oihane Crucelaegui - AvanzOSC
# (c) 2016 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Project Partner Event Registration",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "OdooMRP team",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
    ],
    "category": "Project management",
    "depends": [
        "base",
        "project",
        "event",
        "project_events",
    ],
    "data": [
        "views/project_view.xml",
        "views/event_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
