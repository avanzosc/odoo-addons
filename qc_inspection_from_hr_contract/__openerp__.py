# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Qc Inspection Hr Contract",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    "category": "Quality control",
    "depends": [
        "hr_contract",
        "quality_control",
    ],
    "data": [
        "data/qc_inspection_from_hr_contract_data.xml",
        "views/hr_contract_view.xml",
    ],
    "installable": True,
}
