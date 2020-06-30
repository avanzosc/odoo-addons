# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_text = fields.Text(string='Invoice text',
                               comodel_name='account.fiscal.position',
                               related='fiscal_position_id.invoice_text',
                               store=True)
