# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Lost Object",
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
        "stock",
    ],
    "data": [
        "data/sequence.xml",
        "data/pesa_data.xml",
        "wizard/get_object_view.xml",
        "wizard/give_object_view.xml",
        "wizard/move_object_view.xml",
        "views/lost_object_view.xml",
    ],
    "installable": True,
}
