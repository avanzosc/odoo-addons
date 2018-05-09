# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import tools
from openerp import models, fields


class AnalyticEntriesReport(models.Model):
    _inherit = "analytic.entries.report"

    headquarters_id = fields.Many2one(
        comodel_name='res.headquarters', string='Headquarter')
    product_categ_id = fields.Many2one(
        string="Product category", comodel_name='product.category')

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'analytic_entries_report')
        cr.execute("""
            create or replace view analytic_entries_report as (
                 select
                     min(a.id) as id,
                     count(distinct a.id) as nbr,
                     a.date as date,
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
                     a.product_categ_id as product_categ_id,
                     a.headquarters_id as headquarters_id,
                     sum(a.amount) as amount,
                     sum(a.unit_amount) as unit_amount
                 from
                     account_analytic_line a, account_analytic_account analytic
                 where analytic.id = a.account_id
                 group by
                     a.date, a.user_id, a.name, analytic.partner_id,
                     a.company_id, a.currency_id, a.account_id,
                     a.general_account_id, a.journal_id, a.move_id,
                     a.product_id, a.product_uom_id, a.product_categ_id,
                     a.headquarters_id)
        """)
