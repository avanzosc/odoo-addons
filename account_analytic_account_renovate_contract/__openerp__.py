# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Account Analytic Account Renovate Contract",
    "version": "8.0.1.2.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Sales Management",
    "depends": [
        "account_analytic_analysis"
    ],
    "data": [
        "views/account_analytic_account_view.xml",
        "wizard/wiz_analytic_account_renovate_contract_view.xml",
    ],
    "installable": True,
}
