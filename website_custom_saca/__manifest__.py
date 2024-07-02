# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Custom Saca",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "custom_descarga",
        "custom_saca",
        "custom_saca_purchase",
        "portal",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security_saca.xml",
        "views/mail_templates.xml",
        "report/driver_saca_report.xml",
        "views/templates.xml",
        "views/views.xml",
        "data/email_templates.xml",
    ],
    "installable": True,
}
