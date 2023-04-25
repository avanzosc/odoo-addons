# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Custom Saca",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "custom_descarga",
        "custom_saca",
        "portal",
    ],
    "data": [
        "security/security_saca.xml",
        "views/mail_templates.xml",
        "data/email_templates.xml",
        "report/driver_saca_report.xml",
        "views/templates.xml",
        "views/views.xml"
    ],
    "installable": True,
}
