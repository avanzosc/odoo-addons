# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EventEvent(models.Model):
    _inherit = 'event.event'

    count_survey_participations = fields.Integer(
        string='Survey participations',
        compute='_compute_count_survey_participations',
        compute_sudo=True)

    def _compute_count_survey_participations(self):
        for event in self:
            survey_user_inputs = event._find_survey_inputs()
            event.count_survey_participations = len(survey_user_inputs)

    def button_show_survey_user_input(self):
        self.ensure_one()
        if self.count_survey_participations > 0:
            action = self.env.ref(
                'survey.action_survey_user_input')
            action_dict = action and action.read()[0]
            action_dict["context"] = safe_eval(
                action_dict.get("context", "{}"))
            survey_user_inputs = self._find_survey_inputs()
            if survey_user_inputs:
                domain = expression.AND([
                    [("id", "in", survey_user_inputs.ids)],
                    safe_eval(action.domain or "[]")])
                action_dict.update({"domain": domain})
                return action_dict

    def _find_survey_inputs(self):
        survey_user_input_obj = self.env['survey.user_input']
        surveys = survey_user_input_obj
        responsibles = self.env['res.users']
        if self.main_responsible_id:
            responsibles += self.main_responsible_id
        if self.main_responsible_id:
            responsibles += self.second_responsible_id
        if responsibles:
            cond = [('event_id', '=', self.id),
                    ('main_responsible_id', '!=', False),
                    ('main_responsible_id', 'in', responsibles.ids)]
            survey_user_inputs = survey_user_input_obj.search(cond)
            for survey_user_input in survey_user_inputs:
                if survey_user_input not in surveys:
                    surveys += survey_user_input
            cond = [('event_id', '=', self.id),
                    ('second_responsible_id', '!=', False),
                    ('second_responsible_id', 'in', responsibles.ids)]
            survey_user_inputs = survey_user_input_obj.search(cond)
            for survey_user_input in survey_user_inputs:
                if survey_user_input not in surveys:
                    surveys += survey_user_input
        return surveys
