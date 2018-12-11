# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    _inherit = 'res.partner'

    success_story_count = fields.Integer(
        string='# Success Stories', compute='_compute_success_story_count')

    @api.multi
    def _compute_success_story_count(self):
        story_model = self.env['res.partner.success_story']
        for partner in self:
            partner.success_story_count = story_model.search_count([
                ('partner_id', '=', partner.id)])

    @api.multi
    def button_open_success_stories(self):
        self.ensure_one()
        action = self.env.ref(
            'partner_success_story.res_partner_success_story_action')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'default_partner_id': self.id,
            'hide_partner_id': True,
        })
        domain = expression.AND([
            [('partner_id', '=', self.id)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
