# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "L10n Es Aeat Mod347 Ext",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Localisation/Accounting",
    "depends": [
        "l10n_es_aeat_mod347",
        "mail",
        "report"
    ],
    "data": [
        "security/mod_347_security.xml",
        "report/res_partner_mod347_report.xml",
        "data/l10n_es_aeat_mod347_data.xml",
        "views/l10n_es_aeat_mod347_partner_record_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
