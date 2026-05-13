# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Quality Control Reference Value",
    "summary": "Reference value on test and inspection lines.",
    "category": "Quality Control",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["quality_control_oca"],
    "data": [
        "views/qc_inspection_line_views.xml",
        "views/qc_inspection_views.xml",
        "views/qc_test_question_views.xml",
        "views/qc_test_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "quality_control_reference_value/static/img/icon.png",
        ],
    },
    "installable": True,
}
