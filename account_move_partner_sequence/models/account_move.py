# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    partner_account_seq_id = fields.Many2one(
        string="Account Sequence",
        comodel_name="ir.sequence",
        related="partner_id.account_sequence_id",
        store=True,
    )

    def action_generate_partner_ref(self):
        self.ensure_one()
        if (
            self.partner_id
            and (self.move_type == "in_invoice")
            and not self.ref
            and self.state == "draft"
        ):
            if not self.partner_id.account_sequence_id:
                raise ValidationError(_("The partner has no account sequence."))
            else:
                self.ref = self.partner_id.account_sequence_id.next_by_id()
