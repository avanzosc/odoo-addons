# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class WizAnalyticAccountRenovateContract(models.TransientModel):
    _name = 'wiz.analytic.account.renovate.contract'
    _description = 'Wizard for renovate sale contract'

    increase = fields.Float(
        string='Increase', digits=(1, 3), required=True, default=0.014,
        help='By default an increase in the unit price of 1.4%')

    @api.multi
    def renovate_contracts(self):
        self._search_contracts()._renovate_contract_from_wizard(self.increase)

    def _search_contracts(self):
        contracts = self.env['account.analytic.account'].browse(
            self.env.context.get('active_ids')).filtered(
            lambda x: x.date and (x.type == 'contract' or not x.type))
        return contracts
