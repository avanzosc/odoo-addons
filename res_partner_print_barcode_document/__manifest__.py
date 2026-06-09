# Copyright 2026 AvanzOSC - Alfredo de la Fuente
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Res Partner Print Barcode Document",
    "version": "14.0.1.0.0",
    "category": "Sales/CRM",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["account", "stock"],
    "data": [
        "views/res_partner_view.xml",
        "report/report_picking.xml",
        "report/report_account_invoice.xml",
    ],
    "installable": True,
}
