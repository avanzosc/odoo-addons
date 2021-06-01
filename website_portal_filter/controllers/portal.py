
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website.controllers.main import QueryURL


class CustomerPortal(CustomerPortal):

    @http.route()
    def portal_my_orders(self, page=1, date_begin=None, date_end=None,
                         sortby=None, search_in='all', **kw):
        res = super(CustomerPortal, self).portal_my_orders(
            page, date_begin, date_end, sortby, **kw)
        SaleOrder = request.env['sale.order']
        default_url = '/my/orders'

        domain = self.get_base_sale_domain()

        all_orders = SaleOrder.sudo().search(domain)

        order_partner_ids = None
        if all_orders:
            order_partner_ids = all_orders.mapped('partner_id')

        domain += self.filter_data(kw, 'orders')

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

        keep, args = self.get_keep_url(default_url, kw)

        # pager
        pager = portal_pager(
            url=default_url,
            url_args=args,
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

        _date = args['_date']
        if not _date:
            _date = 'year'
        res.qcontext.update({
            'orders': orders,
            'domain': domain,
            'default_url': default_url,
            'keep': keep,
            'pager': pager,
            'search_in': search_in,
            'date_from': args['date_from'],
            'date_to': args['date_to'],
            'search': args['search'],
            'date':  _date,
            'customer': args['customer'],
            'searchbar_inputs': searchbar_inputs,
            # 'searchbar_filters': [],
            'partner_ids': order_partner_ids,
            'filterby': args['filterby'],
            'date_filters': date_filters,
            'show_date_from_to': True
        })
        return res

    def get_base_sale_domain(self):
        user = request.env.user
        domain = [
            ('state', 'in', ['sale', 'done']),
            ('partner_id', '=', user.partner_id.id)
        ]
        return domain

    @http.route()
    def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None,
                                  sortby=None, filterby=None, **kw):
        res = super(CustomerPortal, self).portal_my_quotes(
            page, date_begin, date_end, sortby, **kw)
        SaleOrder = request.env['purchase.order']
        default_url = '/my/purchase'

        domain = self.get_base_purchase_domain()
        all_orders = SaleOrder.sudo().search(domain)

        order_partner_ids = None
        if all_orders:
            order_partner_ids = all_orders.mapped('partner_id')

        domain += self.filter_data(kw, 'orders')

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

        keep, args = self.get_keep_url(default_url, kw)

        # pager
        pager = portal_pager(
            url=default_url,
            url_args=args,
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

        _date = args['_date']
        if not _date:
            _date = 'year'
        res.qcontext.update({
            'orders': orders,
            'domain': domain,
            'keep': keep,
            'default_url': default_url,
            'pager': pager,
            'date_from': args['date_from'],
            'date_to': args['date_to'],
            'search': args['search'],
            'date':  _date,
            'customer': args['customer'],
            'searchbar_inputs': searchbar_inputs,
            # 'searchbar_filters': [],
            'partner_ids': order_partner_ids,
            'filterby': args['filterby'],
            'date_filters': date_filters,
            'show_date_from_to': True
        })
        return res

    def get_base_purchase_domain(self):
        user = request.env.user
        domain = [
            ('user_id', '=', user.id),
            ('state', 'in', ['purchase', 'done', 'cancel'])
        ]
        return domain

    @http.route()
    def portal_my_invoices(self, page=1, date_begin=None, date_end=None,
                           sortby=None, search_in='all', **kw):
        res = super(CustomerPortal, self).portal_my_invoices(
            page, date_begin, date_end, sortby, **kw)
        AccountInvoice = request.env['account.invoice']
        default_url = "/my/invoices"

        domain = self.get_base_invoice_domain()
        all_invoices = AccountInvoice.sudo().search(domain)
        domain += self.filter_data(kw, 'invoices')

        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        searchbar_sortings = res.qcontext.get('searchbar_sortings')
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        keep, args = self.get_keep_url(default_url, kw)

        # count for pager
        invoice_count = AccountInvoice.search_count(domain)
        # pager
        pager = portal_pager(
            url=default_url,
            url_args=args,
            total=invoice_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        invoices = AccountInvoice.search(
            domain, order=order, limit=self._items_per_page,
            offset=pager['offset'])
        request.session['my_invoices_history'] = invoices.ids[:100]
        invoice_partner_ids = all_invoices.mapped('partner_id').sorted(
            key=lambda r: str(r.name)) if invoices else None
        res.qcontext.update({
            'invoices': invoices,
            'keep': keep,
            'pager': pager,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'search': args['search'],
            'date_from': args['date_from'],
            'date_to': args['date_to'],
            'show_date_from_to': True,
            'customer': args['customer'],
            'partner_ids': invoice_partner_ids,
        })

        return res

    def get_base_invoice_domain(self):
        user = request.env.user
        domain = [
            ('state', 'not in', ('draft', 'cancel')),
            ('partner_id', '=', user.partner_id.id)]
        return domain

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

    def filter_data(self, args, model):
        domain = []

        if 'customer' in args and args.get('customer') not in ['all', '']:
            domain += [('partner_id', '=', int(args.get('customer')))]

        if 'search' in args and args.get('search') != '':
            search = args.get('search')
            if model == 'invoices':
                domain += ['|', ('name', 'ilike', search), '|',
                           ('partner_id.name', 'ilike', search),
                           ('number', 'ilike', search)
                           ]
            else:
                domain += ['|', ('name', 'ilike', search),
                           ('partner_id.name', 'ilike', search)]

        if 'date' in args and args.get('date') not in ['all', '']:
            _date = args.get('date')
            date_filters = self._get_date_filters()
            domain += date_filters[_date]['domain']

        if 'date_from' in args and args.get('date_from') != '':
            date_from = datetime.strptime(
                args.get('date_from'), DEFAULT_SERVER_DATE_FORMAT)
            if model == 'invoices':
                domain += [("date_invoice", '>=', date_from)]
            if model == 'orders':
                domain += [("date_order", '>=', date_from)]

        if 'date_to' in args and args.get('date_to') != '':
            date_to = datetime.strptime(
                args.get('date_to'), DEFAULT_SERVER_DATE_FORMAT)
            if model == 'invoices':
                domain += [("date_invoice", '<=', date_to)]
            if model == 'orders':
                domain += [("date_order", '<=', date_to)]

        return domain

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()

        values['purchase_count'] = request.env['purchase.order'].search_count(
            self.get_base_purchase_domain()
        ) if request.env['purchase.order'].check_access_rights(
            'read', raise_exception=False) else 0

        values['order_count'] = request.env['sale.order'].search_count(
            self.get_base_sale_domain()
        ) if request.env['sale.order'].check_access_rights(
            'read', raise_exception=False) else 0

        values['invoice_count'] = request.env['account.invoice'].search_count(
            self.get_base_invoice_domain()
        ) if request.env['account.invoice'].check_access_rights(
            'read', raise_exception=False) else 0

        return values

    def get_keep_url(self, default_url, kw):

        date_to = kw.get('date_to') if 'date_to' in kw else None
        date_from = kw.get('date_from') if 'date_from' in kw else None
        search = kw.get('search') if 'search' in kw else None
        _date = kw.get('date') if 'date' in kw else None
        customer = kw.get('customer') if 'customer' in kw else 'all'
        filterby = kw.get('filterby') if 'filterby' in kw else None
        sortby = kw.get('sortby') if 'sortby' in kw else None

        args = {
            'date_from': date_from,
            'date_to': date_to,
            'search': search,
            '_date': _date,
            'customer': customer,
            'filterby': filterby,
            'sortby': sortby
        }

        keep = QueryURL(default_url, date=_date, search=search,
                        customer=customer, sortby=sortby, filterby=filterby,
                        date_to=date_to, date_from=date_from)

        return keep, args

    def filter_by_date(self, orders, args):
        if 'date' in args and args.get('date') not in ['all', '']:
            if args.get('date') == 'month':
                orders = orders.filtered(lambda l: l.is_current_month == 1)
            if args.get('date') == 'year':
                orders = orders.filtered(lambda l: l.is_current_year == 1)
        return orders
