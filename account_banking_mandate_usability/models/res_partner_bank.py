# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    def _check_active_mandate(self):
        self.ensure_one()
        active_mandates = self.mandate_ids.filtered(
            lambda m: m.state in ["draft", "valid"])
        if "force_company" in self.env.context:
            active_mandates = active_mandates.filtered(
                lambda m: m.company_id.id == self.env.context.get(
                    "force_company"))
        return bool(active_mandates)

    def _get_mandate_vals(self):
        self.ensure_one()
        return {
            "partner_bank_id": self.id,
            "partner_id": self.partner_id.id,
            "company_id": (
                self.company_id.id or
                self.env.context.get("force_company") or
                self.env["res.company"]._company_default_get(
                    "account.banking.mandate").id),
        }
