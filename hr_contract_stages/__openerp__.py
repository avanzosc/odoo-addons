# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Hr Contract Stages",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "hr_contract",
    ],
    "category": "Human Resources",
    "data": [
        "data/hr_contract_stage_data.xml",
        "security/ir.model.access.csv",
        "views/hr_contract_stages_view.xml",
        "views/hr_contract_view.xml",
    ],
    "installable": True,
    "post_init_hook": "assign_contract_stage",
}
