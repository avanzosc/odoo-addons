# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Import Wizard History",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "sale_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/sale_import_wizard_history_security.xml",
        "views/sale_order_import_views.xml",
        "views/sale_order_import_line_views.xml",
        "views/sale_order_line_history_report_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
