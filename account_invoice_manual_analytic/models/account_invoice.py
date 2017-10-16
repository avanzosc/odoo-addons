# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    analytic_line_ids = fields.One2many(
        comodel_name='account.analytic.line', inverse_name='from_invoice_id',
        string='Analytic lines.')

    @api.multi
    def action_move_create(self):
        for invoice in self:
            invoice.analytic_line_ids.unlink()
        return super(AccountInvoice, self).action_move_create()

    @api.multi
    def generate_analytic_lines(self):
        for invoice in self:
            if not invoice.date_invoice:
                invoice.date_invoice = fields.Date.context_today(self)
            invoice.analytic_line_ids.unlink()
            res = invoice._get_analytic_lines()
            lines = []
            for line in res:
                if line.get('analytic_lines', False):
                    lines += line.get('analytic_lines')
            invoice.analytic_line_ids = lines
