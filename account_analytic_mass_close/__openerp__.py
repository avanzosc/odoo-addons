# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Analytic Mass Close",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Sales Management",
    "depends": [
        "analytic",
        "hr_timesheet_invoice"
    ],
    "data": [
        "data/account_analytic_mass_close_data.xml",
        "wizard/wiz_close_analytic_account_contract_view.xml",
    ],
    "installable": True,
}
