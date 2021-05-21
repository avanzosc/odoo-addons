# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Contact employment info",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Sales/CRM",
    "depends": [
        "contacts"
    ],
    "data": [
            "security/ir.model.access.csv",
            "views/res_partner_views.xml",
            "views/res_partner_employment_situation_views.xml",
            "views/res_partner_expectation_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
