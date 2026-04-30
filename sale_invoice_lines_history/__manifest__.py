# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# Copyright (c) 2026 Eñaut Alberdi - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Invoice Lines History",
    "version": "18.0.1.0.0",
    "depends": [
        "account",
        "base",
        "sale",
        "sale_management",
    ],
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "summary": "Historical sale and invoice lines with list and pivot views",
    "website": "https://github.com/avanzosc/odoo-addons",
    "data": [
        "views/invoice_history_view.xml",
        "views/sale_history_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
