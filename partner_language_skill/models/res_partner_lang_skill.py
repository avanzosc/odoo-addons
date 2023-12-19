# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResPartnerLanguageSkill(models.Model):
    _name = 'res.partner.lang.skill'
    _description = 'Partner Language Skill'
    _rec_name = 'lang_skill_id'

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', required=True)
    lang_skill_id = fields.Many2one(
        comodel_name='res.lang.skill', string='Language Skill', required=True)
    exam_date = fields.Date(required=True)
    obtained = fields.Boolean()

    @api.multi
    def button_mark_obtained(self):
        self.write({
            'obtained': True,
        })
