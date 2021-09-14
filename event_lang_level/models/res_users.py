# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    lang_ids = fields.Many2many(
        string='Languages', comodel_name='hr.skill',
        relation='rel_user_language', column1='user_id', column2='lang_id')

    @api.model
    def create(self, values):
        user = super(ResUsers, self).create(values)
        if user.partner_id:
            user.catch_user_languages()
        return user

    def catch_user_languages(self):
        for user in self:
            langs = self.env['hr.skill']
            employee_skills = user.employee_id.employee_skill_ids.filtered(
                lambda x: x.skill_type_id.skill_language)
            for employee_skills in employee_skills:
                if employee_skills.skill_id not in langs:
                    langs += employee_skills.skill_id
            user.lang_ids = [(6, 0, langs.ids)]
            if user.partner_id:
                user.partner_id.lang_ids = [(6, 0, langs.ids)]
