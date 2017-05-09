# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def automatic_close_analytic_accounts_contract(self):
        cond = [('date', '!=', False),
                ('date', '<=', fields.Date.today()),
                ('state', '=', 'open'),
                ('type', '=', 'contract')]
        self.search(cond).set_close()
