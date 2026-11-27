# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    def _prepare_account_payment_vals(self):
        result = super()._prepare_account_payment_vals()
        result.update({"date": self.date})
        return result
