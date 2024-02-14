# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Survey Building Type Section",
    "version": "16.0.1.1.0",
    "category": "Marketing/Surveys",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "res_partner_building_type_section",
        "survey",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/survey_invite_views.xml",
        "views/survey_question_normative_views.xml",
        "views/survey_question_views.xml",
        "views/survey_user_input_views.xml",
        "views/survey_user_input_line_views.xml",
        "views/survey_survey_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
