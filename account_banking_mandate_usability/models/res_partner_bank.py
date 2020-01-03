# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    @api.multi
    def generate_account_banking_mandate(self):
        mandate_obj = self.env["account.banking.mandate"]
        for bank in self:
            if not bank._check_active_mandate():
                mandate_obj.create(bank._get_mandate_vals())

    @api.multi
    def _check_active_mandate(self):
        self.ensure_one()
        active_mandates = self.mandate_ids.filtered(
            lambda m: m.state in ["draft", "valid"])
        return bool(active_mandates)

    @api.multi
    def _get_mandate_vals(self):
        self.ensure_one()
        return {
            "partner_bank_id": self.id,
            "partner_id": self.partner_id.id,
            "company_id": (
                self.company_id.id or
                self.env["res.company"]._company_default_get(
                    "account.banking.mandate").id),
        }
