# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "CRM phonecall inbound",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Sales/CRM",
    "depends": [
        "contacts",
        "crm_phonecall"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_phonecall_inbound_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
