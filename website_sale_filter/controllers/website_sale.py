
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner_and_orders = self.get_partners_by_connected_user('sale.order')
        values.update({
            'order_partner_ids': list(set(partner_and_orders['partners'])),
            'order_count': len(partner_and_orders['model_objs'])
        })
        return values

    @http.route(['/my/orders', '/my/orders/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_orders(self, page=1, date_begin=None, date_end=None,
                         sortby=None, **kw):
        res = super(CustomerPortal, self).portal_my_orders(
            page, date_begin, date_end, sortby, **kw)
        SaleOrder = request.env['sale.order']
        domain = self.get_domain_by_connected_user(date_begin, date_end,
                                                   'sale.order')
        if not sortby:
            sortby = 'date'
        order = res.qcontext['searchbar_sortings'][sortby]['order']
        filtered_orders = self.filter_data(domain, 'sale.order', **kw)
        filtered_order_ids = []
        for _order in filtered_orders:
            filtered_order_ids.append(_order.id)
        domain += [('id', 'in', filtered_order_ids)]
        order_count = SaleOrder.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        pager = self.recalculatePager(pager, **kw)
        orders = SaleOrder.sudo().search(
            domain, order=order, limit=self._items_per_page,
            offset=pager['offset'])
        res.qcontext.update({
            'orders': orders,
            'pager': pager})
        return res
