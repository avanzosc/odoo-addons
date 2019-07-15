# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResPartnerLanguageSkill(models.Model):
    _name = 'res.partner.lang.skill'
    _description = 'Partner Language Skill'

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', required=True)
    lang_skill_id = fields.Many2one(
        comodel_name='res.lang.skill', string='Language Skill', required=True)
    exam_date = fields.Date(required=True)
    obtained = fields.Boolean()
