# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        if self.move_type == "in_invoice" and self.ref:
            cond = [
                ("partner_id", "=", self.partner_id.id),
                ("invoice_date", "=", self.invoice_date),
                ("ref", "=", self.ref),
                ("id", "!=", self.id),
            ]
            invoice = self.search(cond, limit=1)
            if invoice:
                raise ValidationError(
                    _(
                        "Invoice '%s' exists for the same supplier, date, and "
                        "invoice reference."
                    )
                    % invoice.name
                )
        return super().action_post()
