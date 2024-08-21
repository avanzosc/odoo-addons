# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _risk_account_groups(self):
        super(ResPartner, self)._risk_account_groups()
        max_date = self._max_risk_date_due()
        company_domain = self._get_risk_company_domain()
        return {
            "draft": {
                "domain": company_domain
                + [
                    ("move_id.move_type", "in", ["out_invoice", "out_refund"]),
                    ("account_internal_type", "=", "receivable"),
                    ("parent_state", "in", ["draft", "proforma", "proforma2"]),
                ],
                "fields": ["partner_id", "account_id", "amount_residual"],
                "group_by": ["partner_id", "account_id"],
            },
            "open": {
                "domain": company_domain
                + [
                    ("reconciled", "=", False),
                    ("account_internal_type", "=", "receivable"),
                    ("date_maturity", "!=", False),
                ],
                "fields": ["partner_id", "account_id", "amount_residual"],
                "group_by": ["partner_id", "account_id"],
            },
            "unpaid": {
                "domain": company_domain
                + [
                    ("reconciled", "=", False),
                    ("account_internal_type", "=", "receivable"),
                    "&",
                    ("date_maturity", "=", False),
                    ("date", "<", max_date),
                    ("parent_state", "=", "posted"),
                ],
                "fields": ["partner_id", "account_id", "amount_residual"],
                "group_by": ["partner_id", "account_id"],
            },
        }
