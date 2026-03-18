# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EventEvent(models.Model):
    _inherit = "event.event"

    count_survey_participations = fields.Integer(
        string="Survey participations",
        compute="_compute_count_survey_participations",
        compute_sudo=True,
    )

    def _compute_count_survey_participations(self):
        for event in self:
            survey_user_inputs = event._find_survey_inputs()
            event.count_survey_participations = len(survey_user_inputs)

    def button_show_survey_user_input(self):
        self.ensure_one()
        survey_user_inputs = self._find_survey_inputs()
        if survey_user_inputs:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "survey.action_survey_user_input"
            )
            domain = expression.AND(
                [
                    [("id", "in", survey_user_inputs.ids)],
                    safe_eval(action.get("domain") or "[]"),
                ]
            )
            action.update(
                {
                    "domain": domain,
                }
            )
            return action

    def _find_survey_inputs(self):
        survey_user_input_obj = self.env["survey.user_input"]
        surveys = survey_user_input_obj
        responsibles = self.env["res.users"]
        if self.main_responsible_id:
            responsibles += self.main_responsible_id
        if self.main_responsible_id:
            responsibles += self.second_responsible_id
        if responsibles:
            cond = [
                ("event_id", "=", self.id),
                ("main_responsible_id", "!=", False),
                ("main_responsible_id", "in", responsibles.ids),
            ]
            survey_user_inputs = survey_user_input_obj.search(cond)
            for survey_user_input in survey_user_inputs:
                if survey_user_input not in surveys:
                    surveys += survey_user_input
            cond = [
                ("event_id", "=", self.id),
                ("second_responsible_id", "!=", False),
                ("second_responsible_id", "in", responsibles.ids),
            ]
            survey_user_inputs = survey_user_input_obj.search(cond)
            for survey_user_input in survey_user_inputs:
                if survey_user_input not in surveys:
                    surveys += survey_user_input
        return surveys

    def _create_slide_channels_surveys(self):
        for record in self.mapped("registration_ids").filtered(
            lambda r: r.student_id and r.state not in ["draft", "cancel"]
        ):
            record.create_student_in_courses()

    def _fix_slide_channels_surveys(self):
        for record in self.mapped("registration_ids").filtered(
            lambda r: r.student_id and r.state not in ["draft", "cancel"]
        ):
            survey_inputs = record._find_survey_inputs()
            survey_inputs.fix_slide_partner_relation()


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def create_student_in_courses(self):
        res = super().create_student_in_courses()
        channel_partners = self.env["slide.channel.partner"].search(
            [
                ("event_registration_id", "=", self.id),
            ]
        )
        channel_partners._create_slide_channel_survey()
        return res
