import werkzeug

from odoo import SUPERUSER_ID, _, http
from odoo.exceptions import UserError
from odoo.http import content_disposition, request

from odoo.addons.survey.controllers.main import Survey
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class Survey(Survey):
    @http.route(
        ["/survey/<int:survey_id>/get_evaluation"],
        type="http",
        auth="user",
        methods=["GET"],
        website=True,
    )
    def survey_get_evaluation(self, survey_id, **kwargs):
        """The certification document can be downloaded as long as the user has succeeded the certification"""
        survey = (
            request.env["survey.survey"]
            .sudo()
            .search([("id", "=", survey_id), ("certification", "=", True)])
        )

        if not survey:
            # no certification found
            return werkzeug.utils.redirect("/")

        succeeded_attempt = (
            request.env["survey.user_input"]
            .sudo()
            .search(
                [
                    ("student_id", "=", request.env.user.partner_id.id),
                    ("survey_id", "=", survey_id),
                    ("scoring_success", "=", True),
                ],
                limit=1,
            )
        )
        if not succeeded_attempt:
            succeeded_attempt = (
                request.env["survey.user_input"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", request.env.user.partner_id.id),
                        ("survey_id", "=", survey_id),
                        ("scoring_success", "=", True),
                    ],
                    limit=1,
                )
            )

        if not succeeded_attempt:
            raise UserError(_("The user has not succeeded the certification"))

        return self._generate_eval_report(succeeded_attempt, download=True)

    def _generate_eval_report(self, user_input, download=True):
        report = (
            request.env.ref("slide_channel_survey.action_report_evaluate_certification")
            .with_user(SUPERUSER_ID)
            ._render_qweb_pdf([user_input.id], data={"report_type": "pdf"})[0]
        )

        report_content_disposition = content_disposition("Evaluation.pdf")
        if not download:
            content_split = report_content_disposition.split(";")
            content_split[0] = "inline"
            report_content_disposition = ";".join(content_split)

        return request.make_response(
            report,
            headers=[
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(report)),
                ("Content-Disposition", report_content_disposition),
            ],
        )


class WebsiteSlidesSurvey(WebsiteSlides):
    # OVERRIDDEN
    def _get_users_certificates(self, users):
        partner_ids = [user.partner_id.id for user in users]
        domain = [
            ("scoring_success", "=", True),
            "|",
            ("student_id", "in", partner_ids),
            "&",
            ("student_id", "=", False),
            ("partner_id", "in", partner_ids),
        ]
        certificates = request.env["survey.user_input"].sudo().search(domain)
        users_certificates = {
            user.id: [
                certificate
                for certificate in certificates
                if certificate.partner_id == user.partner_id
                or certificate.student_id == user.partner_id
            ]
            for user in users
        }
        return users_certificates

    def _get_users_certificates_2(self, users):
        partner_ids = [user.partner_id.id for user in users]
        domain = [
            ("scoring_success", "=", True),
            "|",
            ("student_id", "in", partner_ids),
            "&",
            ("student_id", "=", False),
            ("partner_id", "in", partner_ids),
        ]
        certificates = request.env["survey.user_input"].sudo().search(domain)
        return certificates

    def _prepare_user_slides_profile(self, user):
        values = super()._prepare_user_slides_profile(user)
        users_certificates = self._get_users_certificates_2(user)
        values.update({"certificates": users_certificates})
        return values
