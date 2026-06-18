# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Custom Saca",
    "version": "18.0.1.0.0",
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
        "report/driver_saca_report.xml",
        "views/templates.xml",
        "views/views.xml",
        "data/email_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_custom_saca/static/src/js/script.esm.js",
            "website_custom_saca/static/src/css/style.css",
        ],
        "web.report_assets_common": [
            "website_custom_saca/static/src/css/style.css",
        ],
    },
    "installable": True,
}
