# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import Warning
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _compute_contracts_count(self):
        for sale in self:
            sale.contracts_count = len(sale.contract_ids)

    contract_ids = fields.One2many(
        comodel_name='contract.contract',
        inverse_name='sale_id', string='Recurring contracts')
    contracts_count = fields.Integer(
        string='Contracts', compute='_compute_contracts_count')

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            recurrent_lines = sale.order_line.filtered(
                lambda l: l.product_id.recurrent_punctual)
            if any(recurrent_lines.filtered(
                    lambda l: not l.originator_id or not l.payer_ids)):
                raise Warning(_('You must select originator and payers.'))
            for line in recurrent_lines:
                line.create_contract_analytic_invoice_line()
        return res

    @api.multi
    def action_view_contracts(self):
        self.ensure_one()
        action = self.env.ref('contract.action_customer_contract')
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [('sale_id', 'in', self.ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({
            'domain': domain,
        })
        return action_dict


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def create_contract_analytic_invoice_line(self):
        contract_obj = self.env['contract.contract']
        for payer in self.payer_ids:
            cond = [('company_id', '=', self.originator_id.id),
                    ('partner_id', '=', payer.payer_id.id),
                    ('sale_id', '=', self.order_id.id)]
            contract = contract_obj.search(cond, limit=1)
            if not contract:
                contract = self.create_contract(payer)
            line_vals = {
                'contract_id': contract.id,
                'product_id': self.product_id.id,
                'name': self.product_id.name,
                'payment_percentage': payer.pay_percentage,
                'price_unit': self.price_unit,
                'quantity': self.product_uom_qty,
                'uom_id': self.product_id.uom_id.id}
            if self.product_id.recurrent_punctual == 'recurrent':
                self.create_contract_analytic_invoice_line_for_recurrent_produ(
                    line_vals)
            else:
                self.create_contract_analytic_invoice_line_for_months(
                    self.product_id.punctual_month_ids, line_vals)

    def create_contract(self, payer):
        contract_obj = self.env['contract.contract']
        cond = [('type', '=', 'sale'),
                ('company_id', '=', self.company_id.id)]
        journal = self.env['account.journal'].search(cond, limit=1)
        name = "{} - {} - {}".format(
            self.order_id.name, self.originator_id.name,
            payer.payer_id.name)
        contract_vals = {
            'name': name,
            'company_id': self.originator_id.id,
            'partner_id': payer.payer_id.id,
            'sale_id': self.order_id.id,
            'pricelist_id': self.order_id.pricelist_id.id,
            'contract_type': 'sale',
            'journal_id': journal.id}
        if self.order_id.academic_year_id:
            contract_vals.update({
                'academic_year_id': self.order_id.academic_year_id.id,
                'date_end': self.order_id.academic_year_id.date_end})
        if self.order_id.child_id:
            contract_vals['child_id'] = self.order_id.child_id.id
        if self.order_id.school_id:
            contract_vals['school_id'] = self.order_id.school_id.id
        if self.order_id.course_id:
            contract_vals['course_id'] = self.order_id.course_id.id
        contract = contract_obj.create(contract_vals)
        return contract

    def create_contract_analytic_invoice_line_for_recurrent_produ(self, vals):
        line_obj = self.env['contract.line']
        academic_date_start = self.order_id.academic_year_id.date_start
        academic_date_end = self.order_id.academic_year_id.date_end
        date_start = academic_date_start.replace(
            month=self.product_id.month_start.number, day=1)
        date_end = academic_date_end.replace(
            month=self.product_id.end_month.number, day=1)
        # year_from = int(fields.Date.from_string(
        #     self.order_id.academic_year_id.date_start).year)
        # year_to = int(fields.Date.from_string(
        #     self.order_id.academic_year_id.date_end).year)
        # date_start = "{}-{}-01".format(
        #     year_from, str(self.product_id.month_start.number).zfill(2))
        # date_end = "{}-{}-01".format(
        #     year_to, str(self.product_id.end_month.number).zfill(2))
        vals.update({
            'date_start': date_start,
            'date_end': date_end,
            'discount': self.discount,
        })
        line_obj.create(vals)

    def create_contract_analytic_invoice_line_for_months(self, months, vals):
        line_obj = self.env['contract.line']
        date = fields.Date.context_today(self)
        year = int(fields.Date.context_today(self).year)
        for month in months:
            date = "{}-{}-01".format(year+1 if month.number <= 8 else year,
                                     str(month.number).zfill(2))
            vals.update({
                'date_start': date,
                'date_end': date,
                'discount': self.discount,
            })
            line_obj.create(vals)
