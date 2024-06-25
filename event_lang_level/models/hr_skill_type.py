# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class HrSkillType(models.Model):
    _inherit = "hr.skill.type"

    skill_language = fields.Boolean(string="Skill is a language ", default=False)

    @api.model
    def create(self, values):
        result = super().create(values)
        if "skill_language" in values:
            self.env["res.users"].search([]).catch_user_languages()
        return result

    def write(self, values):
        result = super().write(values)
        if "skill_language" in values:
            self.env["res.users"].search([]).catch_user_languages()
        return result
