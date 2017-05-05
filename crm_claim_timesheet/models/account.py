# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    timesheet_ids = fields.One2many(
        comodel_name='hr.analytic.timesheet', string='Timesheets',
        inverse_name='account_id')
