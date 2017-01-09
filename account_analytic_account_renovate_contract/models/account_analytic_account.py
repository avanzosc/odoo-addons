# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _renovate_contract_from_wizard(self, increase):
        for contract in self:
            vals = {'date_start': (fields.Date.from_string(contract.date) +
                                   relativedelta(days=1)),
                    'date': (fields.Date.from_string(contract.date) +
                             relativedelta(years=1))}
            contract.copy(vals)._update_new_contract_renovate_information(
                contract, increase)
            contract.set_close()

    def _update_new_contract_renovate_information(self, origin_contract,
                                                  increase):
        self.name = '{} {}'.format(
            origin_contract.name,
            fields.Date.from_string(self.date_start).year)
        if increase:
            for line in self.recurring_invoice_line_ids.filtered(
                    lambda x: x.price_unit):
                line.price_unit = (line.price_unit +
                                   (line.price_unit * increase))
        self.set_open()
