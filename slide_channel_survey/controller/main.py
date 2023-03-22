
import werkzeug
from odoo import fields, http, SUPERUSER_ID, _
from odoo.http import request, content_disposition
from odoo.addons.survey.controllers.main import Survey
from odoo.exceptions import UserError


class Survey(Survey):

    @http.route(['/survey/<int:survey_id>/get_evaluation'], type='http', auth='user', methods=['GET'], website=True)
    def survey_get_evaluation(self, survey_id, **kwargs):
        """ The certification document can be downloaded as long as the user has succeeded the certification """
        survey = request.env['survey.survey'].sudo().search([
            ('id', '=', survey_id),
            ('certification', '=', True)
        ])

        if not survey:
            # no certification found
            return werkzeug.utils.redirect("/")

        succeeded_attempt = request.env['survey.user_input'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('survey_id', '=', survey_id),
            ('scoring_success', '=', True)
        ], limit=1)

        if not succeeded_attempt:
            raise UserError(_("The user has not succeeded the certification"))

        return self._generate_eval_report(succeeded_attempt, download=True)

    def _generate_eval_report(self, user_input, download=True):
        report = request.env.ref('slide_channel_survey.action_report_evaluate_certification').with_user(SUPERUSER_ID)._render_qweb_pdf([user_input.id], data={'report_type': 'pdf'})[0]

        report_content_disposition = content_disposition('Evaluation.pdf')
        if not download:
            content_split = report_content_disposition.split(';')
            content_split[0] = 'inline'
            report_content_disposition = ';'.join(content_split)

        return request.make_response(report, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(report)),
            ('Content-Disposition', report_content_disposition),
        ])
