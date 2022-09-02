
from odoo.http import request
from odoo import http, _
from odoo.addons.survey.controllers.main import Survey
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        surveys_count = request.env['survey.user_input'].search_count([
            ('partner_id', 'in', [partner.id] or partner.child_ids.ids)
        ])
        values.update({
            'surveys_count': surveys_count
        })
        return values

    @http.route('/my/surveys', type='http', auth='user', website=True)
    def survey_inputs(self, **post):
        values = {}
        partner = request.env.user.partner_id
        partner_ids = partner.child_ids.ids + partner.ids
        survey_inputs = request.env['survey.user_input'].sudo().search([
            '|',
            ('partner_id', 'in', partner_ids),
            ('student_id', 'in', partner_ids)

        ])
        searchbar_sortings = {
            'event': {'label': _('Event'), 'order': 'event_id desc'},
            'survey': {'label': _('Survey'), 'order': 'survey_id'},
        }
        values.update({
            'page_name': 'survey_inputs',
            'survey_inputs': survey_inputs,
            'searchbar_sortings': searchbar_sortings,
            'sortby': 'event',
        })
        return http.request.render(
            'website_survey.portal_my_survey_inputs',
            values)

    @http.route('/my/survey/<model("survey.user_input"):survey_input>', type='http', auth='user', website=True)
    def survey_input(self, survey_input, **post):
        values = {}
        partner = request.env.user.partner_id
        print_url = survey_input.action_print_answers()
        print_certification_url = survey_input.action_print_certification()
        values.update({
            'page_name': 'survey_inputs',
            'survey_input': survey_input,
            'print_url': print_url.get('url'),
            'print_certification_url': print_certification_url.get('url')
        })
        return http.request.render(
            'website_survey.website_survey_input',
            values)


class Survey(Survey):

    @http.route('/survey/certification/print/<string:survey_token>', type='http', auth='public', website=True, sitemap=False)
    def certification_print(self, survey_token, review=False, answer_token=None, **post):
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=False, check_partner=False)
        if access_data['validity_code'] is not True and (
                access_data['has_survey_access'] or
                access_data['validity_code'] not in ['token_required', 'survey_closed', 'survey_void']):
            return self._redirect_with_error(access_data, access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']

        return CustomerPortal()._show_report(
            model=answer_sudo, report_type='pdf',
            report_ref='website_survey.report_califications', download=True)
