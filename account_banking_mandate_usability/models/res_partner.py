# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    bank_acc_count = fields.Integer(
        compute="_compute_bank_acc_count",
        string="Number of Bank accounts",
        readonly=True,
    )
    error_bank_acc = fields.Boolean(
        string="Bank account error",
        compute="_compute_partner_validate_bank_account",
    )

    def _compute_bank_acc_count(self):
        bank_acc_data = self.env["res.partner.bank"].read_group(
            [("partner_id", "in", self.ids)], ["partner_id"], ["partner_id"]
        )
        mapped_data = {
            bank_acc["partner_id"][0]: bank_acc["partner_id_count"]
            for bank_acc in bank_acc_data
        }
        for partner in self:
            partner.bank_acc_count = mapped_data.get(partner.id, 0)

    @api.depends("bank_ids")
    def _compute_partner_validate_bank_account(self):
        for record in self:
            record.error_bank_acc = False
            if not record.bank_ids or any(record.mapped("bank_ids.error_bank_acc")):
                record.error_bank_acc = True

    def create_validate_bank_account_mandate(self):
        if self.bank_ids:
            bank_id = self.env["res.partner.bank"].search(
                [("id", "in", self.bank_ids.ids)], order="id desc", limit=1
            )
            if bank_id:
                if bank_id.error_bank_acc:
                    raise ValidationError(
                        _("The customer does not have a valid bank account.")
                    )
                else:
                    if not bank_id.mandate_ids:
                        bank_id.create_validate_bank_account_mandate()
        else:
            raise ValidationError(_("The customer does not have a bank account."))
