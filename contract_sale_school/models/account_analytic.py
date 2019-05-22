# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = 'account.analytic.invoice.line'

    recurrent_punctual = fields.Selection(
        string='Recurrent/Punctual', related='product_id.recurrent_punctual')
