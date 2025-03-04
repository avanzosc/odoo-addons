# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def copy_data(self, default=None):
        if "from_reverse_moves" in self.env.context:
            for invoice in self:
                default["invoice_user_id"] = invoice.invoice_user_id.id
        return super().copy_data(default=default)
