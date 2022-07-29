
from odoo.http import request
from odoo import http
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
        values.update({
            'survey_inputs': survey_inputs,
        })
        return http.request.render(
            'website_survey.portal_my_survey_inputs',
            values)

    @http.route('/my/survey/<model("survey.user_input"):survey_input>', type='http', auth='user', website=True)
    def survey_input(self, survey_input, **post):
        values = {}
        partner = request.env.user.partner_id
        print_url = survey_input.action_print_answers()
        values.update({
            'survey_input': survey_input,
            'print_url': print_url.get('url')
        })
        return http.request.render(
            'website_survey.website_survey_input',
            values)
