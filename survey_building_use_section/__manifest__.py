# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Survey Building Use Section",
    "version": "16.0.1.1.0",
    "category": "Marketing/Surveys",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "res_partner_building_use_section",
        "survey",
        "survey_input_equipment",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/survey_invite_views.xml",
        "views/add_matrix_article_filter.xml",
        "views/add_question_image_to_survey.xml",
        "views/remove_retake_option.xml",
        "views/survey_question_answer_views.xml",
        "views/survey_question_article_views.xml",
        "views/survey_question_normative_views.xml",
        "views/survey_question_views.xml",
        "views/survey_user_input_views.xml",
        "views/survey_user_input_line_views.xml",
        "views/survey_survey_views.xml",
        "views/installed_equipment_views.xml",
    ],
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "survey_building_use_section/static/src/js/*.js",
            "survey_building_use_section/static/src/js/*.xml",
        ],
    },
}
