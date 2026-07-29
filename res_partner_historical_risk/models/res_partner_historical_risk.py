# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerHistoricalRisk(models.Model):
    _name = "res.partner.historical.risk"
    _description = "Partner Historical Risk"

    partner_id = fields.Many2one(
        string="Contact", comodel_name="res.partner", readonly=True
    )
    commercial_partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="partner_id.commercial_partner_id",
        store=True,
    )
    sale_type = fields.Many2one(
        comodel_name="sale.order.type", related="partner_id.sale_type", store=True
    )
    company_id = fields.Many2one(
        comodel_name="res.company", related="partner_id.company_id", store=True
    )
    date = fields.Date(readonly=True)
    risk_total_amount = fields.Float(string="Amount Risk")
    credit_policy_amount = fields.Float(readonly=True)
