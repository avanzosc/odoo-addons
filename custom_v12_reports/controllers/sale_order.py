
from odoo import api, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public",
                website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None,
                          message=False, download=False, report_number=None,
                          **kw):
        res = super(CustomerPortal, self).portal_order_page(
            order_id, report_type, access_token, message, download, **kw)
        try:
            order_sudo = self._document_check_access(
                'sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text') and report_number:
            report_ref = self.getCoasSaleOrderReportType(report_number)
            return self._show_report(
                model=order_sudo, report_type=report_type,
                report_ref=report_ref,
                download=download)
        return res

    @http.route([
        '/my/orders/<int:order_id>/accept_order'],
                type='json',
                auth="public", website=True)
    def portal_order_accept(self, res_id, access_token=None, partner_name=None,
                            signature=None, order_id=None, report_number=None):
        try:
            order_sudo = self._document_check_access('sale.order', res_id,
                                                     access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order')}
        if not signature:
            return {'error': _('Signature is missing.')}

        self.signCoasSaleOrderReportType(partner_name, signature,
                                         str(report_number), order_sudo)
        print(report_number, 'hola')

#         report_ref = self.getCoasSaleOrderReportType(str(report_number))
#         pdf = request.env.ref(report_ref).sudo(
#             ).render_qweb_pdf([order_sudo.id])[0]
#         _message_post_helper(
#             res_model='sale.order',
#             res_id=order_sudo.id,
#             message=_('Order signed by %s') % (partner_name,),
#             attachments=[('%s.pdf' % order_sudo.name, pdf)],
#             **({'token': access_token} if access_token else {}))

        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(
                query_string='&message=sign_ok'),
        }

    def getCoasSaleOrderReportType(self, report_number):
        if report_number == '1':
            return 'custom_v12_reports.sale_order_full_report'
        elif report_number == '2':
            return 'custom_v12_reports.sale_order_report'
        elif report_number == '3':
            return 'custom_v12_reports.sale_order_report2'
        elif report_number == '4':
            return 'custom_v12_reports.sale_order_report3'
        elif report_number == '5':
            return 'custom_v12_reports.sale_order_report4'
        elif report_number == '6':
            return 'custom_v12_reports.sale_order_report5'
        elif report_number == '7':
            return 'custom_v12_reports.school_issue_report'
        elif report_number == '8':
            return 'custom_v12_reports.school_issue_report2'

    def signCoasSaleOrderReportType(self, partner_name, signature,
                                    report_number, order_sudo):
        if report_number == '1':
            order_sudo.coas_report_1_signature = signature
            order_sudo.coas_report_1_signed_by = partner_name
        elif report_number == '2':
            order_sudo.coas_report_2_signature = signature
            order_sudo.coas_report_2_signed_by = partner_name
        elif report_number == '3':
            order_sudo.coas_report_3_signature = signature
            order_sudo.coas_report_3_signed_by = partner_name
        elif report_number == '4':
            order_sudo.coas_report_4_signature = signature
            order_sudo.coas_report_4_signed_by = partner_name
        elif report_number == '5':
            order_sudo.coas_report_5_signature = signature
            order_sudo.coas_report_5_signed_by = partner_name
        elif report_number == '6':
            order_sudo.coas_report_6_signature = signature
            order_sudo.coas_report_6_signed_by = partner_name
        elif report_number == '7':
            order_sudo.coas_report_7_signature = signature
            order_sudo.coas_report_7_signed_by = partner_name
        elif report_number == '8':
            order_sudo.coas_report_8_signature = signature
            order_sudo.coas_report_8_signed_by = partner_name
