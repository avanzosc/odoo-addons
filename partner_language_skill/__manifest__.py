# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Language Skill",
    "version": "12.0.1.0.0",
    "category": "Contacts",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/res_lang_skill_view.xml",
        "views/res_partner_lang_skill_view.xml",
        "views/res_partner_view.xml",
        "wizards/res_partner_lang_skill_creator_view.xml",
    ],
    "installable": True,
}
