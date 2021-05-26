
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalStock(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalStock, self)._prepare_portal_layout_values()
        partner_and_stocks = self.get_partners_by_connected_user(
            'stock.picking')
        values.update({
            'stock_partner_ids': list(set(partner_and_stocks['partners'])),
            'stock_count': len(partner_and_stocks['model_objs']),
            'stock_picking_ids': partner_and_stocks['model_objs'],
        })
        return values

    @http.route(['/my/stock', '/my/stock/<int:stock_picking_id>',
                 '/my/stock/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_stock(self, stock_picking_id=None, page=1, access_token=None,
                        report_type=None, message=False, download=False, **kw):
        # Prepare values
        values = {'page_name': 'stock'}
        Stock = request.env['stock.picking']
        Stock_move = request.env['stock.move']

        domain = [('partner_id', '=', request.env.user.partner_id.id)]
        stock_count = Stock.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/stock",
            total=stock_count,
            page=page,
            step=self._items_per_page
        )
        pager = self.recalculatePager(pager, **kw)
        stocks = Stock.sudo().search(
            domain, limit=self._items_per_page,
            offset=pager['offset'])

        if stock_picking_id is None:
            values.update({
                'pager': pager,
                'default_url': '/my/stock',
                'stock_picking_ids': stocks
            })
            return request.render("website_stock.portal_my_stock", values)
        else:
            try:
                stock_picking_sudo = self._document_check_access(
                    'stock.picking', stock_picking_id,
                    access_token=access_token)
            except (AccessError, MissingError):
                return request.redirect('/my')

            if report_type in ('html', 'pdf', 'text'):
                return self._show_report(
                    model=stock_picking_sudo, report_type=report_type,
                    report_ref='stock.action_report_picking',
                    download=download)

            body = _('Stock picking viewed by customer')
            _message_post_helper(
                res_model='stock.picking', res_id=stock_picking_sudo.id,
                message=body, token=stock_picking_sudo.access_token,
                message_type='notification', subtype="mail.mt_note",
                partner_ids=[stock_picking_sudo.partner_id.id])

            stock_move_ids = Stock_move.sudo().search([
                ('picking_id', '=', stock_picking_id)
                ])
            stock_picking_id = Stock.browse(
                stock_picking_id)
            values.update({
                'stock_picking_id': stock_picking_id,
                'stock_move_ids': stock_move_ids})
            return request.render("website_stock.portal_my_stock_details",
                                  values)

    @http.route(['/my/stock/<int:stock_picking_id>/accept'], type='json',
                auth="public", website=True)
    def portal_stock_accept(self, res_id, access_token=None, partner_name=None,
                            signature=None, stock_picking_id=None):
        try:
            stock_picking_sudo = self._document_check_access(
                'stock.picking',
                res_id,
                access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid stock picking')}

        if not stock_picking_sudo.has_to_be_signed():
            return {'error': _('Stock picking is not in a' +
                               'state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        stock_picking_sudo.signature = signature
        stock_picking_sudo.signed_by = partner_name

        Stock_Picking_Report = request.env.ref('stock.action_report_picking')
        pdf_1 = Stock_Picking_Report.sudo().render_qweb_pdf(
            [stock_picking_sudo.id])[0]
        pdf_2 = Stock_Picking_Report.sudo().render_qweb_pdf(
            [stock_picking_sudo.id])[0]

        _message_post_helper(
            res_model='stock.picking',
            res_id=stock_picking_sudo.id,
            message=_('Stock picking signed by %s') % (partner_name,),
            attachments=[('%s.pdf' % stock_picking_sudo.name, pdf_1),
                         ('%s.pdf' % stock_picking_sudo.name, pdf_2)],
            **({'token': access_token} if access_token else {}))

        return {
            'force_refresh': True,
            'redirect_url': stock_picking_sudo.get_portal_url(
                query_string='&message=sign_ok')
        }
