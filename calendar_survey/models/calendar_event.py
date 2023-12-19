# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
from odoo.addons.calendar.models.calendar import calendar_id2real_id


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    user_input_ids = fields.One2many(
        comodel_name='survey.user_input', inverse_name='event_id')
    user_input_count = fields.Integer(
        compute='_compute_user_input_count')

    @api.multi
    def _compute_user_input_count(self):
        for event in self:
            event.user_input_count = len(event.user_input_ids)

    @api.multi
    def button_open_user_input(self):
        self.ensure_one()
        real_id = calendar_id2real_id(self.id)
        self = self.with_context(
            default_calendar_id=real_id, default_deadline=self.start)
        action = self.env.ref('survey.action_survey_user_input')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'default_event_id': real_id,
            'default_deadline': self.start,
        })
        domain = expression.AND([
            [('event_id', '=', real_id)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
