# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'

    hide_company_bank_in_sale_orders = fields.Boolean(
        string='Hide Company bank in sale orders', default=False)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    hide_company_bank_in_sale_orders = fields.Boolean(
        string='Hide Company bank in sale orders', store=True,
        related='payment_mode_id.hide_company_bank_in_sale_orders')
