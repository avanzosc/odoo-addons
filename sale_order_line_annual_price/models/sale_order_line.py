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
            num_days = [line.monday, line.tuesday, line.wednesday,
                        line.thursday, line.friday, line.saturday,
                        line.sunday].count(True)
            num_weeks = [line.week1, line.week2, line.week3, line.week4,
                         line.week5, line.week6].count(True)
            num_months = [line.january, line.february, line.march, line.april,
                          line.may, line.june, line.july, line.august,
                          line.september, line.october, line.november,
                          line.december].count(True)
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
