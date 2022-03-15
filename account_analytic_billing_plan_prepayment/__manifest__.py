# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Analytic Billing Plan Prepayment",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Accounting & Finance",
    "depends": [
        "account_analytic_billing_plan",
    ],
    "data": [
        # "security/ir.model.access.csv",
        # "data/ir_sequence_data.xml",
        # "views/account_analytic_account_view.xml",
        "views/account_analytic_billing_plan_view.xml",
    ],
    "installable": True,
}
