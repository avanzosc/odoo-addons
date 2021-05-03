
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from datetime import date, timedelta
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _get_date_filters(self):
        return {
            'all': {'input': 'all', 'label': _('All dates')},
            'today': {'input': 'today', 'label': _('Today'),
                      'domain': [("date_order", '>=', date.today()),
                                 ("date_order", '<', date.today() +
                                  timedelta(days=1))]},
            'week': {'input': 'week', 'label': _('Last week'),
                     'domain': [('date_order', '<=', date.today()),
                                ('date_order', '>=', date.today()
                                 - timedelta(weeks=1))]},
            'month': {'input': 'month', 'label': _('This month'),
                      'domain': [('is_current_month', '=', 1)]},
            'year': {'input': 'year', 'label': _('This year'),
                     'domain': [('is_current_year', '=', 1)]}
            }

    def filter_data(self, args):
        domain = []

        if 'customer' in args and args.get('customer') != 'all':
            domain += [('partner_id', '=', int(args.get('customer')))]

        if 'search' in args and args.get('search') != '':
            search = args.get('search')
            domain += ['|', ('name', 'ilike', search),
                       ('partner_id.name', 'ilike', search)]

        if 'date' in args and args.get('date') != 'all':
            _date = args.get('date')
            date_filters = self._get_date_filters()
            domain += date_filters[_date]['domain']

        return domain

    @http.route()
    def portal_my_orders(self, page=1, date_begin=None, date_end=None,
                         sortby=None, search_in='all', **kw):
        res = super(CustomerPortal, self).portal_my_orders(
            page, date_begin, date_end, sortby, **kw)
        SaleOrder = request.env['sale.order']

        domain = [
            ('state', 'in', ['sale', 'done'])
        ]
        all_orders = SaleOrder.sudo().search(domain)

        order_partner_ids = None
        if all_orders:
            order_partner_ids = all_orders.mapped('partner_id')

        domain += self.filter_data(kw)

        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = res.qcontext.get('searchbar_sortings')[sortby]['order']

        filtered_orders = self.filter_by_date(all_orders, kw)
        domain += [('id', 'in', filtered_orders.ids)]

        # count for pager
        order_count = SaleOrder.sudo().search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        orders = SaleOrder.sudo().search(
            domain, order=sort_order, limit=self._items_per_page,
            offset=pager['offset'])
        request.session['my_orders_history'] = orders.ids[:100]
        date_filters = self._get_date_filters()
        res.qcontext.update({
            'orders': orders,
            'pager': pager,
            'search_in': search_in,
            'search': kw.get('search'),
            'date':  kw.get('date'),
            'customer': kw.get('customer'),
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': [],
            'order_partner_ids': order_partner_ids,
            'filterby': kw.get('filterby'),
            'date_filters': date_filters,
        })
        return res

    def filter_by_date(self, orders, args):
        if 'date' in args and args.get('date') != 'all':
            if args.get('date') == 'month':
                orders = orders.filtered(lambda l: l.is_current_month == 1)
            if args.get('date') == 'year':
                orders = orders.filtered(lambda l: l.is_current_year == 1)
        return orders
