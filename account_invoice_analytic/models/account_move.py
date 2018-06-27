# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    to_invoice = fields.Many2one(
        comodel_name='hr_timesheet_invoice.factor',
        string='Timesheet Invoicing Ratio',
        help="You usually invoice 100% of the timesheets. But if you mix "
             "fixed price and timesheet invoicing, you may use another "
             "ratio. For instance, if you do a 20% advance invoice (fixed "
             "price, based on a sales order), you should invoice the rest on "
             "timesheet with a 80% ratio.")

    @api.multi
    def create_analytic_lines(self):
        res = super(AccountMoveLine, self).create_analytic_lines()
        for move in self.filtered('to_invoice'):
            move.analytic_lines.write({
                'to_invoice': move.to_invoice.id,
            })
        return res
