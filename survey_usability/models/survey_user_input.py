# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    @api.multi
    def button_respond_survey(self):
        self.ensure_one()
        return self.survey_id.with_context(
            survey_token=self.token).action_start_survey()
