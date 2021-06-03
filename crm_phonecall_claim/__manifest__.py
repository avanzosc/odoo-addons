# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "CRM phonecall claim",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Sales/CRM",
    "depends": [
        "crm_phonecall_inbound",
        "crm_claim"
    ],
    "data": [
        "views/crm_phonecall_inbound_views.xml",
        "views/crm_claim_views.xml"
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
}
