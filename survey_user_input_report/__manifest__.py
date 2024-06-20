# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey User Input Report",
    "version": "16.0.1.0.0",
    "depends": [
        "base",
        "survey",
        "res_partner_building_use_section",
        "survey_building_use_section",
        "survey_question_image",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "category": "Tools",
    "data": [
        "views/answers_template_inspeccion.xml",
        "views/answers_template_verificacion.xml",
        "views/front_page_verificacion.xml",
        "views/front_page_inspeccion.xml",
        "views/survey_pdf_report_inspeccion.xml",
        "views/survey_pdf_report_verificacion.xml",
        "views/paper_format.xml",
    ],
    "installable": True,
}
