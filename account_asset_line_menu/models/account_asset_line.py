# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountAssetLine(models.Model):
    _inherit = "account.asset.line"

    depreciated_value = fields.Monetary(aggregator="max")
    remaining_value = fields.Monetary(aggregator="min")

    @api.depends("amount", "previous_id", "type", "move_check")
    def _compute_values(self):
        result = super()._compute_values()
        for line in self:
            depreciated = line.depreciated_value
            if line.move_check:
                line.depreciated_value = depreciated + line.amount
        return result
