# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Fix Price",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        'project_task_ending',
    ],
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "category": "Project Management",
    "data": [
        "security/ir.model.access.csv",
        "views/invoice_mark_view.xml",
        "views/project_view.xml",
    ],
    "installable": True
}
