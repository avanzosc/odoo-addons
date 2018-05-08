# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Analytic Entries Report Headquarter",
    'version': '8.0.1.0.0',
    'license': "AGPL-3",
    'author': "AvanzOSC",
    'website': "http://www.avanzosc.es",
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    "category": "Accounting & Finance",
    "depends": [
        'account_analytic_utilities',
        'analytic_headquarters'
    ],
    "data": [
        'report/account_analytic_entries_report_view.xml'
    ],
    "installable": True,
}
