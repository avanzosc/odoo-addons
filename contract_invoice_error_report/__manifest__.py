# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Contract Invoice Error Report",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "contract",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/wiz_contract_invoice_error_report_views.xml",
        "views/contract_contract_views.xml",
    ],
    "installable": True,
}
