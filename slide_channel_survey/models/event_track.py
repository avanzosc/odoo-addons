# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EventTrack(models.Model):
    _inherit = 'event.track'

    count_survey_participations = fields.Integer(
        string='Survey participations',
        compute='_compute_count_survey_participations',
        compute_sudo=True)

    def _compute_count_survey_participations(self):
        for track in self:
            survey_user_inputs = track._find_survey_inputs()
            track.count_survey_participations = len(survey_user_inputs)

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
        survey_user_input = survey_user_input_obj
        cond = [('event_id', '=', self.event_id.id)]
        if self.partner_id:
            cond.append([('partner_id', '=', self.partner_id.id)])
        date = self.date.date()
        registrations = self.event_id.registration_ids.filtered(
            lambda x: x.student_id and x.real_date_start and
            date >= x.real_date_start and
            (not x.real_date_end or
             (x.real_date_end and date <= x.real_date_end)))
        partners = registrations.mapped('student_id')
        if partners:
            cond = [('event_id', '=', self.event_id.id),
                    ('student_id', '!=', False),
                    ('student_id', 'in', partners.ids)]
            survey_user_inputs = survey_user_input_obj.search(cond)
            if survey_user_inputs:
                survey_user_input += survey_user_inputs
            cond = [('event_id', '=', self.event_id.id),
                    ('partner_id', '!=', False),
                    ('partner_id', 'in', partners.ids)]
            survey_user_inputs = survey_user_input_obj.search(cond)
            if survey_user_inputs:
                survey_user_input += survey_user_inputs
        return survey_user_input
