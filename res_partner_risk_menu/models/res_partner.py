# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    risk_sum = fields.Float(
        string="Sum of Risk", compute="_compute_risk_sum", store=True
    )
    risk_total_amount = fields.Float(
        string="Amount Risk", compute="_compute_risk_total_amount", store=True
    )
    credit_policy_amount = fields.Float(string="Credit Policy Amount")

    @api.depends(
        "risk_sale_order",
        "risk_invoice_draft",
        "risk_invoice_open",
        "risk_invoice_unpaid",
        "risk_account_amount",
        "risk_account_amount_unpaid",
    )
    def _compute_risk_sum(self):
        for partner in self:
            partner.risk_sum = (
                partner.risk_sale_order
                + partner.risk_invoice_draft
                + partner.risk_invoice_open
                + partner.risk_invoice_unpaid
                + partner.risk_account_amount
                + partner.risk_account_amount_unpaid
            )

    @api.depends(
        "risk_sale_order",
        "risk_invoice_draft",
        "risk_invoice_open",
        "risk_invoice_unpaid",
        "risk_account_amount",
        "risk_account_amount_unpaid",
        "credit_policy_amount",
    )
    def _compute_risk_total_amount(self):
        for partner in self:
            partner.risk_total_amount = (
                partner.risk_sale_order
                + partner.risk_invoice_draft
                + partner.risk_invoice_open
                + partner.risk_invoice_unpaid
                + partner.risk_account_amount
                + partner.risk_account_amount_unpaid
                - partner.credit_policy_amount
            )
