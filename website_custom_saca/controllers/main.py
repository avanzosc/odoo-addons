
from odoo.http import request
from odoo import http, _
from datetime import date
from odoo.addons.portal.controllers.portal import CustomerPortal
import json


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
        saca_type = self.get_saca_types()
        domain = [
            ('stage_id', 'in', saca_type.ids),
            ('driver_id', '=', partner.id)]
        if today:
            today = date.today()
            domain += [('date', '=', today)]
        saca_lines = request.env['saca.line'].sudo().search(domain, order='seq')
        sacas = request.env['saca'].sudo().search([
            ('saca_line_ids', 'in', saca_lines.ids)
        ], order='date desc')
        values.update({
            'page_name': 'saca',
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
        saca_line = request.env['saca.line'].sudo().browse(saca_line_id)
        values_update = {}
        for arg in post:
            values_update.update({arg: post.get(arg)})
        if values_update:
            files = request.httprequest.files
            self.update_saca_line_fields(line=saca_line, update_vals=values_update, files=files)
        saca_lines = request.env['saca.line'].sudo().search([
            ('driver_id', '=', partner.id),
            ('saca_id', '=', saca_line.saca_id.id),
        ], order='seq')
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
        toristas = request.env['res.partner'].sudo().search([
            ("category_id", "=", (
                request.env.ref("custom_descarga.torista_category").id))
        ])
        timesheet_ids = saca_line.timesheet_ids.filtered(lambda t: t.task_id.name in ['Chofer', 'Carga'])
        floor_options = request.env['saca.line'].sudo()._fields['floor'].selection
        floor_options_list = {}
        for floor in floor_options:
            floor_options_list.update({
                floor[0]: floor[1]
            })
        values.update({
            'page_name': 'saca_line',
            'saca_line': saca_line,
            'logged_user': request.env.user,
            'next_saca_line_id': next_saca_line_id,
            'prev_saca_line_id': prev_saca_line_id,
            'access_token': access_token,
            'date_today': date.today(),
            'toristas': toristas,
            'floor_options': floor_options_list,
            'timesheet_ids': timesheet_ids,
        })
        return http.request.render(
            'website_custom_saca.portal_saca_line',
            values)

    @http.route('/saca/line/print/<int:saca_id>', type='http', auth='user', website=True, sitemap=False)
    def saca_line_print(self, saca_id, review=False, answer_token=None, **post):
        saca_line = request.env['saca.line'].sudo().browse(saca_id)
        return CustomerPortal()._show_report(
            model=saca_line, report_type='pdf',
            report_ref='website_custom_saca.action_report_driver_saca', download=True)

    @http.route('/saca/line/send/<int:saca_id>', type='json', auth='public',
                methods=['POST'], website=True, csrf=False)
    def saca_line_send(self, saca_id, **post):
        saca_line = request.env['saca.line'].sudo().browse(saca_id)
        saca_line.action_send_saca_mail()
        redirect_url = "/my/saca/line/" + str(saca_id)
        return {
            'message': "An email with de information has been sended to %s." % saca_line.farm_id.email,
           # 'force_refresh': True,
            'redirect_url': redirect_url,
        }

    def update_saca_line_fields(self, line, update_vals, files=None):
        for value in update_vals:
            new_val = None
            if value in ['btn_start', 'btn_finish']:
                line.set_timesheet_start_stop(value, int(update_vals.get(value)))
                break
            ttype = line.sudo()._fields[value]
            if ttype.type == 'float':
                try:
                    new_val = float(update_vals.get(value)) if update_vals.get(value) != '' else None
                except (ValueError, TypeError):
                    new_val = 0

            if ttype.type in ['integer', 'boolean'] or value == 'torista_id':
                try:
                    new_val = int(update_vals.get(value)) if update_vals.get(value) != '' else None
                except (ValueError, TypeError):
                    new_val = 0

            if ttype.type in ['char', 'text', 'selection']:
                if value == 'floor':
                    if update_vals.get(value) == '0':
                        break
                new_val = update_vals.get(value)

           # if ttype.type == 'binary':
                # files = files.getlist(value)
                # attachment = files.read()
                # new_val = base64.encodestring(attachment)
               # new_val = update_vals.get(value)

            if new_val and getattr(line, value) != new_val:
               line.update({value: new_val})

    @http.route(['/saca/line/<int:saca_line_id>/<int:signer_id>/accept'],
                type='json', auth="public", website=True)
    def portal_saca_line_accept(self, saca_line_id=None, signer_id=None, *args, **kwargs):
        access_token = kwargs.get('access_token')
        res_id = kwargs.get('res_id')
        signature = kwargs.get('signature')
        logged_user = request.env['res.users'].browse(request.session.get('uid'))
        saca_line = request.env['saca.line'].sudo().browse(saca_line_id)
        if not signature:
            return {'error': _('Signature is missing.')}
        signer = request.env['res.partner'].sudo().browse(signer_id)
        self.sign_saca_line(saca_line, signer, signature)
        redirect_url = "/my/saca/line/"+str(saca_line_id)

        return {
            'force_refresh': True,
            'redirect_url': redirect_url,
        }

    def sign_saca_line(self, saca_line_id, signer, signature):
        if saca_line_id:
            if saca_line_id.driver_id == signer:
                saca_line_id.signature_driver = signature
                saca_line_id.date_signature_driver = date.today()

            if saca_line_id.farmer_id == signer:
                saca_line_id.signature_farm = signature
                saca_line_id.date_signature_farm = date.today()

    def get_saca_types(self):
        stage_saca = request.env.ref(
            "custom_saca_purchase.stage_saca",
            raise_if_not_found=False)
        return stage_saca

    @http.route(['/my/saca/line/save/file'], type='http', auth="public", methods=['POST'], website=True)
    def post_file_field(self, **kwargs):
        image_file = kwargs.get("img_origin", False)
        saca_line_id = kwargs.get("saca_line_id", False)
        return json.dumps({'success': True, 'message': "Image uploaded!"})
