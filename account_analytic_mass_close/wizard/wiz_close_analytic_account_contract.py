# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizCloseAnalyticAccountContract(models.TransientModel):
    _name = 'wiz.close.analytic.account.contract'
    _description = 'Wizard for close contracts of analytic accounts'

    @api.multi
    def button_close_analytic_accounts_contracts(self):
        self.ensure_one()
        contracts = self.env['account.analytic.account'].browse(
            self.env.context['active_ids']).filtered(
            lambda x: x.state == 'open')
        contracts.set_close()
