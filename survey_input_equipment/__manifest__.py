# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Survey Input Equipment",
    "version": "16.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "maintenance",
        "survey",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_user_input_views.xml",
    ],
    "installable": True,
}
