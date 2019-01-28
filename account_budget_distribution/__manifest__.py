# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Account Budget Distribution",
    "version": "11.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account_budget",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/crossovered_budget_resume_view.xml",
        "wizards/crossovered_budget_distribution_view.xml",
        "views/crossovered_budget_view.xml",
    ],
    "installable": True,
}
