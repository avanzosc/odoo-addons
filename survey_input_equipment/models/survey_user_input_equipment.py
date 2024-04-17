# Copyright 2024 Alfredo de la Fuente - Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class SurveyUser_inputEquipment(models.Model):
    _name = "survey.user_input.equipment"
    _description = "Equipment For Survey User Input"

    survey_user_input_id = fields.Many2one(
        string="Survey User Input", comodel_name="survey.user_input",
        copy=False,
    )
    equipment_id = fields.Many2one(
        string="Equipment", comodel_name="maintenance.equipment", copy=False,
    )
    equipment_category_id = fields.Many2one(
        string="Equipment Category",
        comodel_name="maintenance.equipment.category",
        related="equipment_id.category_id", store=True, copy=False,
    )
