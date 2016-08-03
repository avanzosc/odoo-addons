# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from collections import defaultdict
from datetime import datetime
from mako.template import Template
from openerp import pooler, _, exceptions
from openerp.report import report_sxw
from openerp.addons.report_webkit import report_helper
from openerp.addons.account_financial_report_webkit.report.\
    common_partner_reports import CommonPartnersReportHeaderWebkit
from openerp.addons.account_financial_report_webkit.report.\
    webkit_parser_header_fix import HeaderFooterTextWebKitParser
from openerp.modules.module import get_module_resource


def get_mako_template(obj, *args):
    template_path = get_module_resource(*args)
    return Template(filename=template_path, input_encoding='utf-8')

report_helper.WebKitHelper.get_mako_template = get_mako_template


class PartnersPaymentReportWebkit(report_sxw.rml_parse,
                                  CommonPartnersReportHeaderWebkit):

    def __init__(self, cr, uid, name, context=None):
        super(PartnersPaymentReportWebkit, self).__init__(
            cr, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr

        company = self.pool.get('res.users').browse(
            self.cr, uid, uid, context=context).company_id
        header_report_name = ' - '.join((_('PARTNER PAYMENT REPORT'),
                                        company.name,
                                        company.currency_id.name))

        footer_date_time = self.formatLang(
            str(datetime.today()), date_time=True)

        self.localcontext.update({
            'cr': cr,
            'uid': uid,
            'report_name': _('Partner Payment Report'),
            'display_account_raw': self._get_display_account_raw,
            'filter_form': self._get_filter,
            'target_move': self._get_target_move,
            'amount_currency': self._get_amount_currency,
            'display_partner_account': self._get_display_partner_account,
            'display_target_move': self._get_display_target_move,
            'additional_args': [
                ('--header-font-name', 'Helvetica'),
                ('--footer-font-name', 'Helvetica'),
                ('--header-font-size', '10'),
                ('--footer-font-size', '6'),
                ('--header-left', header_report_name),
                ('--header-spacing', '2'),
                ('--footer-left', footer_date_time),
                ('--footer-right',
                 ' '.join((_('Page'), '[page]', _('of'), '[topage]'))),
                ('--footer-line',),
            ],
        })

    def _get_move_line_datas(
            self, move_line_ids, order='per.special DESC, date_maturity ASC, '
            'per.date_start ASC, m.name ASC'):
        if not move_line_ids:
            return []
        if not isinstance(move_line_ids, list):
            move_line_ids = [move_line_ids]
        monster = """
            SELECT l.id AS id,
                l.date AS ldate,
                j.name AS jcode ,
                j.type AS jtype,
                l.currency_id,
                l.account_id,
                l.amount_currency,
                l.ref AS lref,
                l.name AS lname,
                COALESCE(l.debit, 0.0) - COALESCE(l.credit, 0.0) AS balance,
                l.debit,
                l.credit,
                l.period_id AS lperiod_id,
                per.code as period_code,
                per.special AS peropen,
                l.partner_id AS lpartner_id,
                p.name AS partner_name,
                m.name AS move_name,
                COALESCE(partialrec.name, fullrec.name, '') AS rec_name,
                COALESCE(partialrec.id, fullrec.id, NULL) AS rec_id,
                m.id AS move_id,
                c.name AS currency_code,
                i.id AS invoice_id,
                i.type AS invoice_type,
                i.number AS invoice_number,
                case when l.date_maturity is null then l.date else
                    l.date_maturity end as date_maturity,
                pm.name as payment_mode,
                pt.name as payment_term,
                a.code as account_code
            FROM account_move_line l
                JOIN account_move m on (l.move_id=m.id)
                LEFT JOIN res_currency c on (l.currency_id=c.id)
                LEFT JOIN account_move_reconcile partialrec
                    on (l.reconcile_partial_id = partialrec.id)
                LEFT JOIN account_move_reconcile fullrec
                    on (l.reconcile_id = fullrec.id)
                LEFT JOIN res_partner p on (l.partner_id=p.id)
                LEFT JOIN account_invoice i on (m.id =i.move_id)
                LEFT JOIN account_period per on (per.id=l.period_id)
                LEFT JOIN account_account a on (a.id=l.account_id)
                LEFT JOIN payment_mode pm on (pm.id=i.payment_mode_id)
                LEFT JOIN account_payment_term pt on (pt.id=i.payment_term)
                JOIN account_journal j on (l.journal_id=j.id)
            WHERE l.id in %s"""
        monster += (" ORDER BY %s" % (order,))
        try:
            self.cursor.execute(monster, (tuple(move_line_ids),))
            res = self.cursor.dictfetchall()
        except Exception:
            self.cursor.rollback()
            raise
        return res or []

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = data['form']['chart_account_id']
        # Account initial balance memoizer
        init_balance_memoizer = {}
        # Reading form
        main_filter = self._get_form_param('filter', data, default='filter_no')
        target_move = self._get_form_param('target_move', data, default='all')
        start_date = self._get_form_param('date_from', data)
        stop_date = self._get_form_param('date_to', data)
        start_period = self.get_start_period_br(data)
        stop_period = self.get_end_period_br(data)
        fiscalyear = self.get_fiscalyear_br(data)
        partner_ids = self._get_form_param('partner_ids', data)
        result_selection = self._get_form_param('result_selection', data)
        chart_account = self._get_chart_account_id_br(data)
        commercial_id = self._get_form_param('commercial_id', data)
        payment_modes = self._get_form_param('payment_mode_ids', data)
        allow_unpaid = self._get_form_param('allow_unpaid', data)
        receives_in_account = self._get_form_param('receives_in_account', data)
        if main_filter == 'filter_no' and fiscalyear:
            start_period = self.get_first_fiscalyear_period(fiscalyear)
            stop_period = self.get_last_fiscalyear_period(fiscalyear)
        # Retrieving accounts
        filter_type = ('payable', 'receivable')
        if result_selection == 'customer':
            filter_type = ('receivable',)
        if result_selection == 'supplier':
            filter_type = ('payable',)
        account_ids = self.get_all_accounts(
            new_ids, exclude_type=['view'], only_type=filter_type)
        if not account_ids:
            raise exceptions.Warning(_('Error: No accounts to print.'))
        if main_filter == 'filter_date':
            start = start_date
            stop = stop_date
        else:
            start = start_period
            stop = stop_period
        if commercial_id:
            domain = [('user_id', '=', commercial_id)]
            if partner_ids:
                domain += [('id', 'in', partner_ids)]
            partner_ids = self.pool.get('res.partner').search(self.cursor,
                                                              self.uid, domain)
        if not partner_ids:
            domain = []
            partner_ids = self.pool.get('res.partner').search(self.cursor,
                                                              self.uid, domain)
        ledger_lines_memoizer = self._compute_open_transactions_lines(
            account_ids, main_filter, target_move, start, stop,
            partner_filter=partner_ids, payment_modes=payment_modes,
            allow_unpaid=allow_unpaid, receives_in_account=receives_in_account)
        objects = self.pool.get('res.partner').browse(self.cursor,
                                                      self.uid,
                                                      partner_ids)
        ledger_lines = {}
        init_balance = {}
        partners_order = {}
        for partner in objects:
            ledger_lines[partner.id] = ledger_lines_memoizer.get(partner.id,
                                                                 {})
            init_balance[partner.id] = init_balance_memoizer.get(partner.id,
                                                                 {})
            # we have to compute partner order based on inital balance
            # and ledger line as we may have partner with init bal
            # that are not in ledger line and vice versa
            ledg_lines_pids = ledger_lines_memoizer.keys()
            non_null_init_balances = dict([
                (ib, amounts) for ib, amounts
                in init_balance[partner.id].iteritems()
                if amounts['init_balance'] or
                amounts['init_balance_currency']])
            init_bal_lines_pids = non_null_init_balances.keys()
            partners_order[partner.id] = self._order_partners(
                ledg_lines_pids, init_bal_lines_pids)
            ledger_lines[partner.id] = ledger_lines_memoizer.get(partner.id,
                                                                 {})
        self.localcontext.update({
            'fiscalyear': fiscalyear,
            'start_date': start_date,
            'stop_date': stop_date,
            'start_period': start_period,
            'stop_period': stop_period,
            'partner_ids': partner_ids,
            'chart_account': chart_account,
            'ledger_lines': ledger_lines,
            'init_balance': init_balance,
            'partners_order': partners_order,
        })
        return super(PartnersPaymentReportWebkit, self).set_context(
            objects, data, new_ids, report_type=report_type)

    def _tree_move_line_partner_ids(self, move_lines_data, key=None):
        res = defaultdict(dict)
        for row in move_lines_data[:]:
            partner_id = row.pop('partner_id')
            if key:
                res[partner_id].append(row[key])
            else:
                res[partner_id] = row
        return res

    def get_partners_move_lines_ids(
            self, account_ids, main_filter, start, stop, target_move,
            exclude_reconcile=False, partner_filter=False):
        filter_from = False
        if main_filter in ('filter_period', 'filter_no'):
            filter_from = 'period'
        elif main_filter == 'filter_date':
            filter_from = 'date'
        if filter_from:
            return self._get_partners_move_line_ids(
                filter_from, account_ids, start, stop, target_move,
                exclude_reconcile=exclude_reconcile,
                partner_filter=partner_filter)

    def _get_partners_move_line_ids(
            self, filter_from, account_ids, start, stop, target_move,
            opening_mode='exclude_opening', exclude_reconcile=False,
            partner_filter=None):
        final_res = defaultdict(list)
        sql_select = "SELECT account_move_line.id, \
                        account_move_line.partner_id FROM account_move_line"
        sql_joins = ''
        sql_where = " WHERE account_move_line.account_id in %(account_ids)s "\
                    " AND account_move_line.state = 'valid' "
        method = getattr(self, '_get_query_params_from_' + filter_from + 's')
        sql_conditions, search_params = method(start, stop)
        sql_where += sql_conditions
        if exclude_reconcile:
            sql_where += ("  AND ((account_move_line.reconcile_id IS NULL)"
                          "   OR (account_move_line.reconcile_id IS NOT NULL\
                              AND account_move_line.last_rec_date > \
                                                      date(%(date_stop)s)))")
        if partner_filter:
            sql_where += "   AND account_move_line.partner_id \
                                                            in %(partner_ids)s"
        if target_move == 'posted':
            sql_joins += "INNER JOIN account_move \
                                ON account_move_line.move_id = account_move.id"
            sql_where += " AND account_move.state = %(target_move)s"
            search_params.update({'target_move': target_move})
        search_params.update({
            'account_ids': tuple(account_ids),
            'partner_ids': tuple(partner_filter),
            })
        sql = ' '.join((sql_select, sql_joins, sql_where))
        self.cursor.execute(sql, search_params)
        res = self.cursor.dictfetchall()
        if res:
            for row in res:
                final_res[row['partner_id']].append(row['id'])
        return final_res

    def _compute_open_transactions_lines(
            self, accounts_ids, main_filter, target_move, start, stop,
            partner_filter=False, payment_modes=False, allow_unpaid=False,
            receives_in_account=False):
        res = defaultdict(dict)
        move_line_obj = self.pool.get('account.move.line')
        if main_filter in ('filter_period', 'filter_no'):
            date_stop = stop.date_stop
        elif main_filter == 'filter_date':
            date_stop = stop
        else:
            raise exceptions.Warning(
                _('Unsuported filter: Filter has to be in filter date, period,'
                  ' or none'))
        initial_move_lines_per_partner = {}
        if main_filter in ('filter_period', 'filter_no'):
            initial_move_lines_per_partner = self._tree_move_line_partner_ids(
                self._partners_initial_balance_line_ids(
                    accounts_ids, start, partner_filter,
                    exclude_reconcile=True, force_period_ids=False,
                    date_stop=date_stop), key='id')
        move_line_ids_per_partner = self.get_partners_move_lines_ids(
            accounts_ids, main_filter, start, stop, target_move,
            exclude_reconcile=True, partner_filter=partner_filter)
        for partner_id in partner_filter:
            partner_line_ids = (
                move_line_ids_per_partner.get(partner_id, []) +
                initial_move_lines_per_partner.get(partner_id, []))
            new_partner_line_ids = False
            load_new = False
            if partner_line_ids:
                load_new = True
                if payment_modes:
                    domain = [('id', 'in', partner_line_ids),
                              ('payment_mode_id', 'in', payment_modes)]
                    new_partner_line_ids = move_line_obj.search(
                        self.cursor, self.uid, domain)
                    jdomain = False
                    if allow_unpaid:
                        jdomain = [('default_credit_account_id.code', 'ilike',
                                    '4315%')]
                    if receives_in_account:
                        if jdomain:
                            jdomain.insert(0, '|')
                            jdomain.insert(0, '|')
                            jdomain += [
                                ('default_credit_account_id.code', 'ilike',
                                 '572%'),
                                ('default_credit_account_id.code', 'ilike',
                                 '570%')]
                        else:
                            jdomain = [
                                '|',
                                ('default_credit_account_id.code', 'ilike',
                                 '572%'),
                                ('default_credit_account_id.code', 'ilike',
                                 '570%')]
                    if jdomain:
                        journals = self.pool['account.journal'].search(
                            self.cursor, self.uid, jdomain)
                        if journals:
                            special_domain = [('id', 'in', partner_line_ids),
                                              ('journal_id', 'in', journals),
                                              ('payment_mode_id', '=', False)]
                            new_partner_line_ids += move_line_obj.search(
                                self.cursor, self.uid, special_domain)
            if load_new:
                partner_line_ids = new_partner_line_ids
            lines = self._get_move_line_datas(list(set(partner_line_ids)))
            if lines:
                res[partner_id] = lines
        return res

HeaderFooterTextWebKitParser(
    'report.account.account_report_partner_payment_webkit',
    'account.account',
    'addons/account_partner_payment_report/report/templates/\
                                        report_partner_payment.mako',
    parser=PartnersPaymentReportWebkit)
