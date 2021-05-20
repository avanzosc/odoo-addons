
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
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

        if 'date_from' in args and args.get('date_from') != '':
            date_from = datetime.strptime(args.get('date_from'), DEFAULT_SERVER_DATE_FORMAT)
            domain += [("date_order", '>=', date_from)]
            print('!!', args.get('date_from'), date_from)

        if 'date_to' in args and args.get('date_to') != '':
            date_to = datetime.strptime(args.get('date_to'), DEFAULT_SERVER_DATE_FORMAT)
            domain += [("date_order", '<=', date_to)]
            print('!!', args.get('date_to'))

        return domain

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values['purchase_count'] = request.env['purchase.order'].search_count([
            ('state', 'in', ['purchase', 'done', 'cancel']),
            ('partner_id', '=', request.env.uid)
        ]) if request.env['purchase.order'].check_access_rights('read', raise_exception=False) else 0
        values['order_count'] = request.env['sale.order'].search_count([
            ('state', 'in', ['sale', 'done']),
            ('partner_id', '=', partner.id)
        ]) if request.env['sale.order'].check_access_rights('read', raise_exception=False) else 0
        return values

    @http.route()
    def portal_my_orders(self, page=1, date_begin=None, date_end=None,
                         sortby=None, search_in='all', **kw):
        res = super(CustomerPortal, self).portal_my_orders(
            page, date_begin, date_end, sortby, **kw)
        SaleOrder = request.env['sale.order']
        default_url = '/my/orders'

        user = request.env.user
        domain = [
            ('state', 'in', ['sale', 'done']),
            ('partner_id', '=', user.partner_id.id)
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

        date_to = None
        if 'date_to' in kw:
            date_to = kw.get('date_to')
        date_from = None
        if 'date_from' in kw:
            date_from = kw.get('date_from')

        res.qcontext.update({
            'orders': orders,
            'domain': domain,
            'default_url': default_url,
            'pager': pager,
            'search_in': search_in,
            'date_from': date_from,
            'date_to': date_to,
            'search': kw.get('search'),
            'date':  kw.get('date') if 'date' in kw else 'all',
            'customer': kw.get('customer') if 'customer'in kw else 'all',
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': [],
            'order_partner_ids': order_partner_ids,
            'filterby': kw.get('filterby'),
            'date_filters': date_filters,
        })
        return res

    @http.route()
    def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        res = super(CustomerPortal, self).portal_my_quotes(
            page, date_begin, date_end, sortby, **kw)
        SaleOrder = request.env['purchase.order']
        default_url = '/my/purchase'

        user = request.env.user
        domain = [
            ('user_id', '=', user.id),
            ('state', 'in', ['purchase', 'done', 'cancel'])
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
            url="/my/purchase",
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

        date_to = None
        if 'date_to' in kw:
            date_to = kw.get('date_to')
        date_from = None
        if 'date_from' in kw:
            date_from = kw.get('date_from')
        res.qcontext.update({
            'orders': orders,
            'domain': domain,
            'default_url': default_url,
            'pager': pager,
            'date_from': date_from,
            'date_to': date_to,
            'search': kw.get('search'),
            'date':  kw.get('date') if 'date' in kw else 'all',
            'customer': kw.get('customer') if 'customer'in kw else 'all',
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': [],
            'order_partner_ids': order_partner_ids,
            'filterby': kw.get('filterby'),
            'date_filters': date_filters,
        })
        return res

    @http.route()
    def portal_my_invoices(self, page=1, date_begin=None, date_end=None,
                         sortby=None, search_in='all', **kw):
        res = super(CustomerPortal, self).portal_my_invoices(
            page, date_begin, date_end, sortby, **kw)
        AccountInvoice = request.env['account.invoice']

        domain = self.filter_data(kw)

        return res

    def filter_by_date(self, orders, args):
        if 'date' in args and args.get('date') != 'all':
            if args.get('date') == 'month':
                orders = orders.filtered(lambda l: l.is_current_month == 1)
            if args.get('date') == 'year':
                orders = orders.filtered(lambda l: l.is_current_year == 1)
        return orders
