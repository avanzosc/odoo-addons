# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class WizAnalyticInvoiceLineIncrease(models.TransientModel):
    _name = 'wiz.analytic.invoice.line.increase'
    _description = 'Wizard for increase analytic account invoice lines'

    increase = fields.Float(
        string='Increase', digits=(1, 3), required=True, default=0.014,
        help='By default an increase in the unit price of 1.4%')

    @api.multi
    def increase_account_invoice_line(self):
        if self.increase:
            contracts = self._search_contracts()
            for line in contracts.mapped(
                'recurring_invoice_line_ids').filtered(
                    lambda x: x.price_unit):
                line.price_unit = (line.price_unit +
                                   (line.price_unit * self.increase))

    def _search_contracts(self):
        contracts = self.env['account.analytic.account'].browse(
            self.env.context.get('active_ids')).filtered(
            lambda x: x.date and (x.type == 'contract' or not x.type) and
                x.recurring_invoice_line_ids)
        return contracts
