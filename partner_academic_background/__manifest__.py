# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner academic background",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Sales/CRM",
    "depends": [
        "contacts",
        "crm_phonecall"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/res_partner_academic_background_views.xml",
        "views/res_partner_academic_year_views.xml",
        "views/res_partner_course_level_views.xml",
        "views/crm_phone_call_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
