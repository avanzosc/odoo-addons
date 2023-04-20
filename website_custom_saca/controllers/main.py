
from odoo.http import request
from odoo import http, _
from datetime import datetime, date
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        today = date.today()
        saca_lines = request.env['saca.line'].sudo().search([
            ('driver_id', '=', partner.id)
        ])
        saca_lines_count_today = saca_lines.filtered(lambda l: l.date == today)
        values.update({
            'saca_lines_count': len(saca_lines),
            'saca_lines_count_today': len(saca_lines_count_today)
        })
        return values

    @http.route(['/my/saca/lines', '/my/saca/lines/all'],
                type='http', auth='user', website=True)
    def saca_lines(self, today=False, **post):
        values = {}
        partner = request.env.user.partner_id
        domain = [('driver_id', '=', partner.id)]
        limit = None
        if today:
            today = date.today()
            domain += [('date', '=', today)]
        saca_lines = request.env['saca.line'].sudo().search(domain)
        sacas = request.env['saca'].sudo().search([
            ('saca_line_ids', 'in', saca_lines.ids)
        ], order='date desc', limit=limit)
        values.update({
            'today': today,
            'partner': partner,
            'sacas': sacas,
            'saca_lines': saca_lines
        })
        return http.request.render(
            'website_custom_saca.portal_my_saca_lines',
            values)

    @http.route(['/my/saca/line/<int:saca_line_id>'], type='http', auth='user', website=True)
    def saca_line(self, saca_line_id=None, access_token=None, download=None, **post):
        values = {}
        partner = request.env.user.partner_id
        saca_line = request.env['saca.line'].sudo().search([
            ('id', '=', saca_line_id)
        ])
        saca_lines = request.env['saca.line'].sudo().search([
            ('driver_id', '=', partner.id),
            ('saca_id', '=', saca_line.saca_id.id),
        ], order='date desc')
        saca_line_ids = saca_lines.ids
        value_index = saca_line_ids.index(saca_line.id)
        try:
            next_saca_line_id = saca_line_ids[value_index+1]
        except IndexError:
            next_saca_line_id = None

        try:
            prev_saca_line_id = saca_line_ids[value_index-1] if value_index else None
        except IndexError:
            prev_saca_line_id = None

        values.update({
            'saca_line': saca_line,
            'next_saca_line_id': next_saca_line_id,
            'prev_saca_line_id': prev_saca_line_id,
            'access_token': access_token,
        })
        return http.request.render(
            'website_custom_saca.portal_saca_line',
            values)

    @http.route('/saca/line/print/<int:saca_id>', type='http', auth='public', website=True, sitemap=False)
    def certification_print(self, saca_id, review=False, answer_token=None, **post):
        saca_line = request.env['saca.line'].sudo().browse(saca_id)
        return CustomerPortal()._show_report(
            model=saca_line, report_type='pdf',
            report_ref='website_custom_saca.action_report_driver_saca', download=True)
