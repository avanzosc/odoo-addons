# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Pesa Custom",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "crm_claim",
        "base_vat",
    ],
    "category": "Custom Modules",
    "data": [
        "security/pesa_security.xml",
        "security/ir.model.access.csv",
        "views/journey_view.xml",
        "views/real_line_view.xml",
        "views/crm_claim_view.xml",
        "views/schedule_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True
}
