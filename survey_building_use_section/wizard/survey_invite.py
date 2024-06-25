# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import re

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError

emails_split = re.compile(r"[;,\n\r]+")


class SurveyInvite(models.TransientModel):
    _inherit = "survey.invite"

    partner_id = fields.Many2one(string="Recipient", comodel_name="res.partner")
    building_to_inspect_id = fields.Many2one(
        string="Building to inspect", comodel_name="res.partner"
    )
    building_with_activation_date = fields.Boolean(
        string="Building with activation date"
    )
    building_activation_date = fields.Date(string="building activation date")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_ids = [(6, 0, self.partner_id.ids)]
        else:
            self.partner_ids = [(6, 0, [])]

    @api.onchange("building_to_inspect_id")
    def _onchange_building_to_inspect_id(self):
        building_with_activation_date = True
        if (
            self.building_to_inspect_id
            and not self.building_to_inspect_id.service_start_date
        ):
            building_with_activation_date = False
        self.building_with_activation_date = building_with_activation_date

    def action_create_building_survey(self):
        self.ensure_one()
        if self.building_activation_date:
            self.building_to_inspect_id.service_start_date = (
                self.building_activation_date
            )
        Partner = self.env["res.partner"]
        valid_partners = self.partner_ids
        langs = set(valid_partners.mapped("lang")) - {False}
        if len(langs) == 1:
            self = self.with_context(lang=langs.pop())
        valid_emails = []
        for email in emails_split.split(self.emails or ""):
            partner = False
            email_normalized = tools.email_normalize(email)
            if email_normalized:
                limit = None if self.survey_users_login_required else 1
                partner = Partner.search(
                    [("email_normalized", "=", email_normalized)], limit=limit
                )
            if partner:
                valid_partners |= partner
            else:
                email_formatted = tools.email_split_and_format(email)
                if email_formatted:
                    valid_emails.extend(email_formatted)
        if not valid_partners and not valid_emails:
            raise UserError(_("Please enter at least one valid recipient."))
        self._prepare_building_answers(valid_partners, valid_emails)

    def _prepare_building_answers(self, partners, emails):
        answers = self.env["survey.user_input"]
        existing_answers = self.env["survey.user_input"].search(
            [
                "&",
                ("survey_id", "=", self.survey_id.id),
                "|",
                ("partner_id", "in", partners.ids),
                ("email", "in", emails),
                ("inspected_building_id", "=", self.building_to_inspect_id.id),
            ]
        )
        partners_done = self.env["res.partner"]
        emails_done = []
        if existing_answers:
            if self.existing_mode == "resend":
                partners_done = existing_answers.mapped("partner_id")
                emails_done = existing_answers.mapped("email")
                for partner_done in partners_done:
                    answers |= next(
                        existing_answer
                        for existing_answer in existing_answers.sorted(
                            lambda answer: answer.create_date, reverse=True
                        )
                        if existing_answer.partner_id == partner_done
                    )
                for email_done in emails_done:
                    answers |= next(
                        existing_answer
                        for existing_answer in existing_answers.sorted(
                            lambda answer: answer.create_date, reverse=True
                        )
                        if existing_answer.email == email_done
                    )
        for new_partner in partners - partners_done:
            answers |= self.survey_id.with_context(
                building=self.building_to_inspect_id
            )._create_answer(
                partner=new_partner, check_attempts=False, **self._get_answers_values()
            )
