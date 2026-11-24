# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        companies._create_personal_name_sequence()
        return companies

    def _create_personal_name_sequence(self):
        sequence_obj = self.env["ir.sequence"]
        for company in self:
            exists = sequence_obj.search(
                [
                    ("code", "=", "account.move.personal.name"),
                    ("company_id", "=", company.id),
                ],
                limit=1,
            )
            if exists:
                continue
            sequence_obj.create(
                {
                    "name": f"Account Move Personal Name ({company.name})",
                    "code": "account.move.personal.name",
                    "padding": 5,
                    "use_date_range": True,
                    "company_id": company.id,
                }
            )
