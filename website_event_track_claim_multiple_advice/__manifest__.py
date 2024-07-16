# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Event Track Claim Multiple Advice",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "category": "Marketing/Events",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "crm_claim",
        "website_event_track_claim",
    ],
    "data": [
        "data/website_event_track_claim_multiple_advice_data.xml",
        "views/crm_claim_category_views.xml",
    ],
    "installable": True,
}
