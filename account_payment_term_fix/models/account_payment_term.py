# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta

from openerp import fields, models


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    def compute(self, cr, uid, id, value, date_ref=False, context=None):
        today = fields.Date.today()
        if not date_ref:
            date_ref = today
        pt = self.browse(cr, uid, id, context=context)
        amount = value
        result = []
        obj_precision = self.pool.get('decimal.precision')
        prec = obj_precision.precision_get(cr, uid, 'Account')
        for line in pt.line_ids:
            if line.value == 'fixed':
                amt = round(line.value_amount, prec)
            elif line.value == 'procent':
                amt = round(value * line.value_amount, prec)
            elif line.value == 'balance':
                amt = round(amount, prec)
            if amt:
                next_date = (fields.Datetime.from_string(date_ref) +
                             relativedelta(days=line.days))
                if line.days2 < 0:
                    # Getting 1st of next month
                    next_first_date = (
                        next_date + relativedelta(day=1, months=1))
                    next_date = (
                        next_first_date + relativedelta(days=line.days2))
                if line.days2 > 0:
                    if next_date.day > line.days2:
                        next_date += relativedelta(day=line.days2, months=1)
                    elif next_date.day <= line.days2:
                        next_date += relativedelta(day=line.days2)
                result.append((fields.Date.to_string(next_date), amt))
                amount -= amt

        amount = reduce(lambda x, y: x + y[1], result, 0.0)
        dist = round(value - amount, prec)
        if dist:
            result.append((today, dist))
        return result
