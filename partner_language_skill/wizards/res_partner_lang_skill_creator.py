# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartnerLangSkillCreator(models.TransientModel):
    _name = 'res.partner.lang.skill.creator'
    _description = 'Partner Language Skill Creation Wizard'

    partner_ids = fields.Many2many(comodel_name='res.partner', required=True)
    lang_id = fields.Many2one(
        string='Language', comodel_name='res.lang.skill', required=True)
    date = fields.Date()

    @api.model
    def default_get(self, fields_list):
        res = super(ResPartnerLangSkillCreator, self).default_get(
            fields_list)
        if self.env.context.get('active_model') == 'res.partner':
            res.update({'partner_ids': self.env.context.get('active_ids')})
        return res

    @api.multi
    def button_create_skills(self):
        self.ensure_one()
        date = self.date or fields.Date.context_today(self)
        for partner in self.partner_ids:
            partner.lang_skill_ids = [(0, 0, {'lang_skill_id': self.lang_id,
                                              'exam_date': date})]
