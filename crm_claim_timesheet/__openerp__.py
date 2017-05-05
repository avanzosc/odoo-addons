# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Timesheet on claims",
    "version": "8.0.1.0.0",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "category": "Custom module",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "project_claims",
        "hr_timesheet",
    ],
    "data": [
        "views/crm_claim_view.xml",
        "views/hr_analytic_timesheet_view.xml",
    ],
    "installable": True,
    "post_init_hook": "assign_claims_to_project",
}
