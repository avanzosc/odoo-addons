# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Descarga Report",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": ["web", "custom_saca", "custom_descarga", "res_company_stamp"],
    "data": [
        "report/saca_report.xml",
        "report/cleaning_certificate_report.xml",
    ],
    "installable": True,
}
