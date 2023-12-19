
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner_and_invoices = self.get_partners_by_connected_user(
            'account.invoice')
        values.update({
            'invoice_partner_ids': list(set(partner_and_invoices['partners'])),
            'invoice_count': len(partner_and_invoices['model_objs'])
        })
        return values

    @http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_invoices(self, page=1, date_begin=None, date_end=None,
                           sortby=None, **kw):
        res = super(CustomerPortal, self).portal_my_invoices(
            page, date_begin, date_end, sortby, **kw)
        AccountInvoice = request.env['account.invoice']
        domain = self.get_domain_by_connected_user(date_begin, date_end,
                                                   'account.invoice')
        if not sortby:
            sortby = 'date'
        order = res.qcontext['searchbar_sortings'][sortby]['order']
        filtered_invoices = self.filter_data(domain, 'account.invoice', **kw)
        filtered_invoices_ids = []
        for invoice in filtered_invoices:
            filtered_invoices_ids.append(invoice.id)
        domain += [('id', 'in', filtered_invoices_ids)]
        invoice_count = AccountInvoice.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/invoices",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby},
            total=invoice_count,
            page=page,
            step=self._items_per_page
        )
        pager = self.recalculatePager(pager, **kw)
        invoices = AccountInvoice.sudo().search(
            domain, order=order, limit=self._items_per_page,
            offset=pager['offset'])
        res.qcontext.update({
            'invoices': invoices,
            'pager': pager})
        return res
