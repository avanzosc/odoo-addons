# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def line_get_convert(self, line, part, date):
        line_dict = super(AccountInvoice, self).line_get_convert(
            line, part, date)
        if line.get('inv_line_id', False):
            line_dict.update({
                'to_invoice': self.env['account.invoice.line'].browse(
                    line['inv_line_id']).to_invoice.id,
            })
        return line_dict


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    to_invoice = fields.Many2one(
        comodel_name='hr_timesheet_invoice.factor',
        string='Timesheet Invoicing Ratio',
        help="You usually invoice 100% of the timesheets. But if you mix "
             "fixed price and timesheet invoicing, you may use another "
             "ratio. For instance, if you do a 20% advance invoice (fixed "
             "price, based on a sales order), you should invoice the rest on "
             "timesheet with a 80% ratio.")

    @api.model
    def move_line_get_item(self, line):
        line_dict = super(AccountInvoiceLine, self).move_line_get_item(line)
        line_dict.update({
            'to_invoice': line.to_invoice.id,
            'inv_line_id': line.id,
        })
        return line_dict
