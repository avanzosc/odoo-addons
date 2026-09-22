# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _historical_risk_vals(self):
        self.ensure_one()
        vals = {
            "partner_id": self.id,
            "date": fields.Date.today(),
            "risk_total_amount": self.risk_total_amount,
            "credit_policy_amount": self.credit_policy_amount,
        }
        return vals

    def _create_historical_risk(self):
        for partner in self:
            historical_risk_obj = self.env["res.partner.historical.risk"]
            values = partner._historical_risk_vals()
            historical_risk_obj.create(values)

    @api.model
    def cron_create_historical_risk(self):
        partners = self.search([("active", "=", True)])
        partners._create_historical_risk()
