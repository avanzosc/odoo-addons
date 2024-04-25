# -*- coding: utf-8 -*-
# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Res Partner CNAE",
    "summary": "Customization Module",
    "version": "16.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_cnae_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
