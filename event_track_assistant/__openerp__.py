# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Event Track Assistant",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "Avanzosc, S.L., "
              "Odoo Community Association (OCA)",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Event Management",
    "depends": [
        "website_event_track",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/wiz_event_append_assistant_view.xml",
        "wizard/wiz_event_delete_assistant_view.xml",
        "views/event_event_view.xml",
        "views/event_registration_view.xml",
        "views/event_track_view.xml",
        "views/event_track_presence_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
