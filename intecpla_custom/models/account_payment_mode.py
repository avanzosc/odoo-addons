# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'

    print_reference_to_payment = fields.Boolean(
        string='Print reference to make payment on customer invoices',
        default=False)
