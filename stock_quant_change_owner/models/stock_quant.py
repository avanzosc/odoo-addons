# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_change_owner(self, owner, quants):
        for quant in quants:
            quant = self.env["stock.quant"].search([("id", "=", quant)], limit=1)
            quant.sudo().owner_id = owner.id
