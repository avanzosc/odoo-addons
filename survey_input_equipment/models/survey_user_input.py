# Copyright 2024 Alfredo de la Fuente - Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SurveyUser_input(models.Model):
    _inherit = "survey.user_input"

    equipment_ids = fields.One2many(
        string="Equipments",
        comodel_name="survey.user_input.equipment",
        inverse_name="survey_user_input_id",
        copy=False,
    )
