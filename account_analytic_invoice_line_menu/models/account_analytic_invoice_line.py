# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = 'account.analytic.invoice.line'

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner',
        related='analytic_account_id.partner_id', store=True, readonly=True)
    analytic_account_parent_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic account parent',
        related='analytic_account_id.parent_id', store=True, readonly=True)
