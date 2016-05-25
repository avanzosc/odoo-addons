# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Crm Claim Security",
    "summary": "",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "crm_claim",
    ],
    "data": [
        "security/crm_claim_security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
