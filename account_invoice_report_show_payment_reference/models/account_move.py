# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    print_payment_reference_in_invoices = fields.Boolean(
        string="Print payment reference in invoices",
        related='payment_mode_id.print_payment_reference_in_invoices')
