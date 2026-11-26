# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    error_bank_acc = fields.Boolean(
        string="Bank account error",
        compute="_compute_validate_bank_account",
    )

    def _check_active_mandate(self):
        self.ensure_one()
        active_mandates = self.mandate_ids.filtered(
            lambda m: m.state in ["draft", "valid"]
        )
        if "force_company" in self.env.context:
            active_mandates = active_mandates.filtered(
                lambda m: m.company_id.id == self.env.context.get("force_company")
            )
        return bool(active_mandates)

    def _get_mandate_vals(self):
        self.ensure_one()
        return {
            "partner_bank_id": self.id,
            "partner_id": self.partner_id.id,
            "company_id": (
                self.company_id.id
                or self.env.context.get("force_company")
                or self.env.company.id
            ),
        }

    @api.depends("acc_type")
    def _compute_validate_bank_account(self):
        for record in self:
            record.error_bank_acc = False
            if record.acc_type not in "iban":
                record.error_bank_acc = True

    def create_validate_bank_account_mandate(self):
        wiz_obj = self.sudo().env["res.partner.bank.mandate.generator"]
        mandate_wiz = wiz_obj.create(
            {
                "bank_ids": [self.id],
                "mandate_format": "sepa",
                "mandate_type": "recurrent",
                "mandate_scheme": "CORE",
                "mandate_recurrent_sequence_type": "recurring",
                "signed": True,
                "validate": True,
            }
        )
        mandate_wiz.button_generate_mandates()
