# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api
from datetime import datetime
from openerp.addons import decimal_precision as dp
from dateutil.relativedelta import relativedelta


class ProductBudgetLine(models.Model):

    _name = 'product.budget.line'

    @api.multi
    def _prac_amt(self):
        self.ensure_one()
        analytic_line_obj = self.env['account.analytic.line']
        self.real_amount = 0.00
        self.real_subtotal = 0.00
        self.real_qty = 0.0
        budget_line = self.budget_line_id
        acc_ids = [x.id for x in budget_line.general_budget_id.account_ids]
        if budget_line.analytic_account_id:
            analytic_line_lst = analytic_line_obj.search(
                [('account_id', '=', budget_line.analytic_account_id.id),
                 ('date', '>=', budget_line.date_from),
                 ('date', '<=', budget_line.date_to),
                 ('general_account_id', 'in', acc_ids),
                 ('product_id', '=', self.product_id.id)])
            qty = sum([x.unit_amount for x in analytic_line_lst])
            subtotal = sum([x.amount for x in analytic_line_lst])
            amount = (sum([(x.amount/x.unit_amount) for x in
                           analytic_line_lst]) / len(analytic_line_lst))
            self.real_amount = amount
            self.real_subtotal = subtotal
            self.real_qty = qty

    @api.one
    @api.depends('budget_line_id', 'budget_line_id.date_from',
                 'budget_line_id.date_to', 'budget_line_id.general_budget_id',
                 'budget_line_id.general_budget_id.account_ids',
                 'budget_line_id.analytic_account_id', 'product_id')
    def _prac(self):
        self.real_amount = 0.00
        self.real_subtotal = 0.00
        self.real_qty = 0.0
        budget_line = self.budget_line_id
        if (budget_line.date_to and budget_line.date_from and
                budget_line.general_budget_id.account_ids):
            self._prac_amt()

    @api.one
    @api.depends('expected_qty', 'expected_price')
    def _get_subtotal(self):
        self.expected_subtotal = self.expected_qty * self.expected_price

    product_id = fields.Many2one('product.product', string='Product')
    account_id = fields.Many2one('account.account', string='Account')
    expected_qty = fields.Float(string='Expected Qty',
                                digits=dp.get_precision('Product UoM'))
    expected_price = fields.Float(string='Unit price',
                                  digits=dp.get_precision('Account'))
    expected_subtotal = fields.Float(string="Expected subtotal",
                                     compute='_get_subtotal', store=True,
                                     digits=dp.get_precision('Account'))
    budget_line_id = fields.Many2one('crossovered.budget.lines',
                                     string='Budget Line', ondelete="cascade")
    real_amount = fields.Float(string='Real Price', compute='_prac',
                               digits=dp.get_precision('Account'))
    real_qty = fields.Float(string='Real Qty', compute='_prac',
                            digits=dp.get_precision('Product UoM'))
    real_subtotal = fields.Float(string='Real Subtotal', compute='_prac',
                                 digits=dp.get_precision('Account'))
    categ_id = fields.Many2one('product.category', string="Product category",
                               related='product_id.categ_id', store=True)
    prod_type = fields.Selection([('product', 'Stockable Product'),
                                  ('consu', 'Consumable'),
                                  ('service', 'Service')],
                                 related='product_id.type',
                                 string="Product type", store=True)
    date_start = fields.Date(string="Date start",
                             related='budget_line_id.date_from', store=True)
    date_end = fields.Date(string="Date end", related='budget_line_id.date_to',
                           store=True)
    period_id = fields.Many2one('account.period', string="Period", store=True,
                                related='budget_line_id.period_id')
    analytic_account = fields.Many2one(
        "account.analytic.account", store=True, string="Analytic account",
        related='budget_line_id.analytic_account_id')
    partner_id = fields.Many2one(
        'res.partner', string='Partner', store=True,
        related='budget_line_id.analytic_account_id.partner_id')
    crossovered_budget_id = fields.Many2one(
        'crossovered.budget', string="Budget", store=True,
        related='budget_line_id.crossovered_budget_id')

    @api.one
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.expected_price = self.product_id.list_price


class CrossoveredBudgetLines(models.Model):

    _inherit = 'crossovered.budget.lines'

    @api.one
    @api.depends('product_budget_ids', 'product_budget_ids.expected_qty',
                 'product_budget_ids.expected_price')
    def _get_amount(self):
        self.general_amount = sum([(x.expected_qty * x.expectd_price) for x in
                                   self.product_budget_ids])

    @api.one
    @api.depends('date_from', 'date_to', 'general_budget_id',
                 'general_budget_id.account_ids')
    def _prac(self):
        if (self.date_from and self.date_to and
                self.general_budget_id.account_ids):
            self._prac_amt()

    @api.one
    @api.depends('date_from', 'date_to', 'general_budget_id',
                 'general_budget_id.account_ids')
    def _theo(self):
        if (self.date_from and self.date_to and
                self.general_budget_id.account_ids):
            self._theo_amt()

    @api.one
    @api.depends('date_from', 'date_to')
    def _es_trimestral(self):
        val = False
        if (self.date_from and self.date_to and
                (fields.Date.from_string(self.date_to).month -
                 fields.Date.from_string(self.date_from).month) > 0):
            val = True
        self.es_trimestral = val

    product_budget_ids = fields.One2many('product.budget.line',
                                         'budget_line_id',
                                         string='Product budget lines',
                                         copy=True)
    partner_id = fields.Many2one("res.partner", string="Partner", store=True,
                                 related='analytic_account_id.partner_id')
    es_trimestral = fields.Boolean(compute='_es_trimestral',
                                   string="Es trimestral")
    period_id = fields.Many2one('account.period', string='Periodo')
    general_amount = fields.Float(string="General amount",
                                  compute='_get_amount',
                                  digits=dp.get_precision('Account'))
    date_from = fields.Date('Start Date', required=False)
    date_to = fields.Date('End Date', required=False)
    theoritical_amount = fields.Float(string='Theoretical Amount',
                                      digits=dp.get_precision('Account'),
                                      compute="_theo")
    practical_amount = fields.Float(string='Practical Amount',
                                    digits=dp.get_precision('Account'),
                                    compute="_prac")

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            cross_name = (rec.crossovered_budget_id and
                          rec.crossovered_budget_id.name_get() or '')
            analytic_acc_name = (rec.analytic_account_id and
                                 rec.analytic_account_id.name_get() or '')
            result.append((rec.id, '%s - %s' % (cross_name,
                                                analytic_acc_name)))
        return result

    @api.multi
    def dividir_meses(self, fecha_inicio, fecha_fin):
        start_date = fields.Date.from_string(self.date_from)
        end_date = fields.Date.from_string(self.date_to)
        date_array = []
        date_diff = end_date.month - start_date.month
        while date_diff >= 0:
            today = start_date + relativedelta(months=date_diff)
            initial_date = datetime(today.year, today.month, 1)
            final_date = (initial_date + relativedelta(months=1) +
                          relativedelta(days=-1))
            date_dict = {'start_month': fields.Date.to_string(initial_date),
                         'end_month': fields.Date.to_string(final_date)}
            date_array.append(date_dict)
            date_diff -= 1
        date_array.reverse()
        return date_array

    @api.multi
    def dividir_trimestres(self):
        self.ensure_one()
        res = []
        period_obj = self.env['account.period']
        date_lst = self.dividir_meses()
        month_count = len(date_lst)
        if date_lst:
            first_date = date_lst.pop(0)
            period_ids = period_obj.find(first_date['start_month'])
            period_lst = period_ids.filtered(lambda x: not x.special)
            write_vals = {'date_from': first_date['start_month'],
                          'date_to': first_date['end_month'],
                          'es_trimestral': False,
                          'period_id': period_lst.id,
                          'planned_amount': self.planned_amount / month_count}
            self.write(write_vals)
            res.append(self.id)
            for pro_line_o in self.product_budget_ids:
                pro_line_o.expected_qty = pro_line_o.expected_qty / month_count
            for date_o in date_lst:
                period_ids = period_obj.find(date_o['start_month'])
                period_lst = period_ids.filtered(lambda x: not x.special)
                line_defaults = {'date_from': date_o['start_month'],
                                 'date_to': date_o['end_month'],
                                 'period_id': period_lst.id}
                new_id = self.copy()
                new_id.write(line_defaults)
                res.append(new_id.id)
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'crossovered.budget.lines',
            'res_id': res,
            'view_id': False,
            'domain': [('id', 'in', res)],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            }

    @api.multi
    def copiar_trimestres(self):
        self.ensure_one()
        res = []
        period_obj = self.env['account.period']
        date_lst = self.dividir_meses()
        if date_lst:
            first_date = date_lst.pop(0)
            period_ids = period_obj.find(first_date['start_month'])
            period_lst = period_ids.filtered(lambda x: not x.special)
            write_vals = {'date_from': first_date['start_month'],
                          'date_to': first_date['end_month'],
                          'es_trimestral': False,
                          'period_id': period_lst.id}
            self.write(write_vals)
            res.append(self.id)
            for date_o in date_lst:
                period_ids = period_obj.find(date_o['start_month'])
                period_lst = period_ids.filtered(lambda x: not x.special)
                line_defaults = {'date_from': date_o['start_month'],
                                 'date_to': date_o['end_month'],
                                 'period_id': period_lst.id}
                new_id = self.copy()
                new_id.write(line_defaults)
                res.append(new_id.id)
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'crossovered.budget.lines',
            'res_id': res,
            'view_id': False,
            'domain': [('id', 'in', res)],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            }

    @api.multi
    def copy_period(self):
        self.ensure_one()
        copy_defaults = {'date_to': False,
                         'date_from': False,
                         'period_id': False
                         }
        new_id = self.copy()
        new_id.write(copy_defaults)
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'crossovered.budget.lines',
            'res_id': [new_id.id],
            'domain': [('id', '=', new_id.id)],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True
            }

    @api.one
    @api.onchange('period_id', 'date_from', 'date_to')
    def onchange_period(self):
        period_obj = self.env['account.period']
        if not self.period_id and self.date_from and self.date_to:
            period_ids = period_obj.find(self.date_from)
            period_lst = period_ids.filtered(lambda x: not x.special)
            self.period_id = period_lst.id
        if self.period_id:
            if not self.date_to or not self.date_from:
                self.date_to = self.period_id.date_stop
                self.date_from = self.period_id.date_start
        if self.date_to and self.date_from:
            if ((fields.Date.from_string(self.date_from).month -
                    fields.Date.from_string(self.date_to).month) > 0):
                self.es_trimestral = True
            else:
                self.es_trimestral = False

    @api.multi
    def load_product_accounts(self):
        for rec in self:
            prod_lst = rec.product_budget_ids
            account_lst = rec.general_budget_id.account_ids.ids
            for prod in prod_lst:
                acc = False
                acc = (prod.product_id.property_account_income or
                       prod.product_id.categ_id.property_account_income_categ)
                account_lst.append(acc.id)
                prod.account_id = acc
                rec.general_budget_id.account_ids = [(6, 0, account_lst)]
