# Copyright 2023 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def generated2uploaded(self):
        result = super(
            AccountPaymentOrder, self.with_context(get_bank_line_communication=True)
        ).generated2uploaded()
        return result

    def _prepare_move_line_partner_account(self, bank_line):
        vals = super()._prepare_move_line_partner_account(
            bank_line
        )
        if (
            "get_bank_line_communication" in self.env.context
            and vals
            and bank_line
            and self.payment_type != "outbound"
        ):
            vals["name"] = bank_line.communication
        return vals
