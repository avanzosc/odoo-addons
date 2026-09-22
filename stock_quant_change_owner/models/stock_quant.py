# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _get_forbidden_fields_write(self):
        forbidden_fields = super()._get_forbidden_fields_write()
        if "owner_id" in forbidden_fields:
            forbidden_fields.remove("owner_id")
        return forbidden_fields

    def action_change_owner(self, owner, quants):
        for quant in quants:
            quant = self.env["stock.quant"].search([("id", "=", quant)], limit=1)
            quant.sudo().owner_id = owner.id
