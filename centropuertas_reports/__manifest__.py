# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Centro Puertas Reports",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "centropuertas_custom",
        "web",
        "account_payment_partner",
        "account_payment_order",
    ],
    "author": "AvanzOSC",
    "website": "https://bitbucket.org/centropuertas/centropuertas/",
    "category": "Custom",
    "data": [
        "report/report_layouts.xml",
        "report/sale_order_report.xml",
        "report/account_move_report.xml",
        "report/account_payment_order_report.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "centropuertas_reports/static/src/scss/primary_variables.scss",
        ],
        "web.report_assets_common": [
            ("include", "web._assets_bootstrap"),
            ('include', 'web._assets_primary_variables'),
            "centropuertas_reports/static/src/scss/custom_layout.scss",
            "centropuertas_reports/static/src/scss/layout_boxed.scss",
        ],
    },
    "installable": True,
}
