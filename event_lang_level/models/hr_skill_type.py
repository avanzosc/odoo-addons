# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class HrSkillType(models.Model):
    _inherit = 'hr.skill.type'

    skill_language = fields.Boolean(
        string='Skill is a language ', default=False)

    @api.model
    def create(self, values):
        result = super(HrSkillType, self).create(values)
        if "skill_language" in values:
            self.env['res.users'].search([]).catch_user_languages()
        return result

    def write(self, values):
        result = super(HrSkillType, self).write(values)
        if "skill_language" in values:
            self.env['res.users'].search([]).catch_user_languages()
        return result
