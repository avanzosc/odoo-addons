# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, tools, _


class AnalyticEntriesReport(models.Model):
    _inherit = "analytic.entries.report"

    month = fields.Selection(
        [('1', _('January')), ('2', _('February')), ('3', _('March')),
         ('4', _('April')), ('5', _('May')), ('6', _('June')),
         ('7', _('July')), ('8', _('August')), ('9', _('September')),
         ('10', _('October')), ('11', _('November')), ('12', _('December'))],
        string='Measure')
    year = fields.Integer(string='Year')
    analytic_journal_id = fields.Many2one(
        comodel_name='account.analytic.journal', string='Analytic journal')

    def _select(self):
        select_str = """
        select
            min(a.id) as id,
            count(distinct a.id) as nbr,
            a.date as date,
            cast(extract(MONTH FROM a.date) as char) as month,
            cast(extract(year from a.date) as integer) as year,
            a.user_id as user_id,
            a.name as name,
            analytic.partner_id as partner_id,
            a.company_id as company_id,
            a.currency_id as currency_id,
            a.account_id as account_id,
            a.general_account_id as general_account_id,
            a.journal_id as journal_id,
            a.move_id as move_id,
            a.product_id as product_id,
            a.product_uom_id as product_uom_id,
            a.journal_id as analytic_journal_id,
            sum(a.amount) as amount,
            sum(a.unit_amount) as unit_amount
        """
        return select_str

    def _from(self):
        from_str = """
        from account_analytic_line a, account_analytic_account analytic
        """
        return from_str

    def _where(self):
        where_str = """
        where analytic.id = a.account_id
        """
        return where_str

    def _group_by(self):
        group_by_str = """
        group by a.date, cast(EXTRACT(MONTH FROM a.date) as char),
                cast(extract(year from a.date) as integer), a.user_id, a.name,
                analytic.partner_id, a.company_id, a.currency_id, a.account_id,
                a.general_account_id, a.journal_id, a.move_id,
                a.product_id, a.product_uom_id, a.journal_id
        """
        return group_by_str

    def _order_by(self):
        order_by_str = """
        order  by 1
        """
        return order_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (%s %s %s %s %s)
        """ % (self._table, self._select(), self._from(), self._where(),
               self._group_by(), self._order_by()))
