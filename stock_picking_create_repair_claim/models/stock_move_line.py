# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def catch_values_from_create_repair_from_picking(self):
        vals = super().catch_values_from_create_repair_from_picking()
        if self.claim_id:
            vals["claim_id"] = self.claim_id.id
        return vals
