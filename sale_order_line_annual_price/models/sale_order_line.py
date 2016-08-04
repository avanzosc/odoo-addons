# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _compute_line_quotes(self):
        for line in self:
            self.weekly_amount = 0
            self.monthly_amount = 0
            self.annual_amount = 0
            self.monthly_quota = 0
            num_days = 0
            num_weeks = 0
            num_months = 0
            if line.monday:
                num_days += 1
            if line.tuesday:
                num_days += 1
            if line.wednesday:
                num_days += 1
            if line.thursday:
                num_days += 1
            if line.friday:
                num_days += 1
            if line.saturday:
                num_days += 1
            if line.sunday:
                num_days += 1
            if line.week1:
                num_weeks += 1
            if line.week2:
                num_weeks += 1
            if line.week3:
                num_weeks += 1
            if line.week4:
                num_weeks += 1
            if line.week5:
                num_weeks += 1
            if line.week6:
                num_weeks += 1
            if line.january:
                num_months += 1
            if line.february:
                num_months += 1
            if line.march:
                num_months += 1
            if line.april:
                num_months += 1
            if line.may:
                num_months += 1
            if line.june:
                num_months += 1
            if line.july:
                num_months += 1
            if line.august:
                num_months += 1
            if line.september:
                num_months += 1
            if line.october:
                num_months += 1
            if line.november:
                num_months += 1
            if line.december:
                num_months += 1
            line.weekly_amount = line.price_subtotal * num_days
            line.monthly_amount = line.price_subtotal * num_days * num_weeks
            line.annual_amount = (line.price_subtotal * num_days * num_weeks *
                                  num_months)
            if line.annual_amount > 0:
                line.monthly_quota = line.annual_amount / 12

    weekly_amount = fields.Float(
        string='Weekly amount', digits=dp.get_precision('Account'),
        compute='_compute_line_quotes')
    monthly_amount = fields.Float(
        string='Monthly amount', digits=dp.get_precision('Account'),
        compute='_compute_line_quotes')
    annual_amount = fields.Float(
        string='Annual amount', digits=dp.get_precision('Account'),
        compute='_compute_line_quotes')
    monthly_quota = fields.Float(
        string='Monthly quota', digits=dp.get_precision('Account'),
        compute='_compute_line_quotes')
