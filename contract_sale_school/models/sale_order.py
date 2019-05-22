# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _compute_contracts_count(self):
        for sale in self:
            sale.contracts_count = len(sale.analytic_account_ids)

    analytic_account_ids = fields.One2many(
        comodel_name='account.analytic.account',
        inverse_name='sale_id', string='Recurring contracts')
    contracts_count = fields.Integer(
        string='Contracts', compute='_compute_contracts_count')

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            for line in sale.order_line.filtered(
                lambda c: c.originator_id and c.payer_ids and
                    c.product_id.recurrent_punctual):
                line.create_account_analytic_invoice_line()
        return res

    @api.multi
    def action_view_contracts(self):
        self.ensure_one()
        return {'name': _('Contracts'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'account.analytic.account',
                'domain': [('sale_id', '=', self.id)],
                'context': self.env.context}


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def create_account_analytic_invoice_line(self):
        account_obj = self.env['account.analytic.account']
        for payer in self.payer_ids:
            cond = [('company_id', '=', self.originator_id.id),
                    ('partner_id', '=', payer.payer_id.id),
                    ('sale_id', '=', self.order_id.id)]
            account = account_obj.search(cond, limit=1)
            if not account:
                account = self.create_account_analytic_account(payer)
            line_vals = {
                'analytic_account_id': account.id,
                'product_id': self.product_id.id,
                'name': self.product_id.name,
                'payment_percentage': payer.pay_percentage,
                'price_unit': self.price_unit,
                'quantity': self.product_uom_qty,
                'uom_id': self.product_id.uom_id.id}
            if self.product_id.recurrent_punctual == 'recurrent':
                self.create_account_analytic_invoice_line_for_recurrent_produ(
                    line_vals)
            else:
                self.create_account_analytic_invoice_line_for_months(
                    self.product_id.punctual_month_ids, line_vals)

    def create_account_analytic_account(self, payer):
        account_obj = self.env['account.analytic.account']
        cond = [('type', '=', 'sale'),
                ('company_id', '=', self.company_id.id)]
        journal = self.env['account.journal'].search(cond, limit=1)
        name = "{} - {} - {}".format(
            self.order_id.name, self.originator_id.name,
            payer.payer_id.name)
        account_vals = {
            'name': name,
            'recurring_invoices': True,
            'company_id': self.originator_id.id,
            'partner_id': payer.payer_id.id,
            'sale_id': self.order_id.id,
            'pricelist_id': self.order_id.pricelist_id.id,
            'contract_type': 'sale',
            'journal_id': journal.id}
        if self.order_id.academic_year_id:
            account_vals.update({
                'academic_year_id': self.order_id.academic_year_id.id,
                'date_start': self.order_id.academic_year_id.date_start,
                'recurring_next_date':
                self.order_id.academic_year_id.date_start,
                'date_end': self.order_id.academic_year_id.date_end})
        if self.order_id.child_id:
            account_vals['child_id'] = self.order_id.child_id.id
        if self.order_id.school_id:
            account_vals['school_id'] = self.order_id.school_id.id
        if self.order_id.course_id:
            account_vals['course_id'] = self.order_id.course_id.id
        account = account_obj.create(account_vals)
        return account

    def create_account_analytic_invoice_line_for_recurrent_produ(self, vals):
        line_obj = self.env['account.analytic.invoice.line']
        year_from = int(fields.Date.from_string(
            self.order_id.academic_year_id.date_start).year)
        year_to = int(fields.Date.from_string(
            self.order_id.academic_year_id.date_end).year)
        date_start = "{}-{}-01".format(
            year_from, str(self.product_id.month_start.number).zfill(2))
        date_end = "{}-{}-01".format(
            year_to, str(self.product_id.end_month.number).zfill(2))
        vals.update({'from_date': date_start,
                     'to_date': date_end,
                     'discount': self.discount})
        line_obj.create(vals)

    def create_account_analytic_invoice_line_for_months(self, months, vals):
        line_obj = self.env['account.analytic.invoice.line']
        year = int(fields.Date.context_today(self).year)
        for month in months:
            date = "{}-{}-01".format(year+1 if month.number <= 8 else year,
                                     str(month.number).zfill(2))
            vals.update({'from_date': date,
                         'to_date': date,
                         'discount': self.discount})
            line_obj.create(vals)
