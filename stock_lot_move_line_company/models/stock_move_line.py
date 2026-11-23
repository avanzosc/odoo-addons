# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _prepare_new_lot_vals(self):
        vals = super()._prepare_new_lot_vals()
        vals.setdefault("company_id", self.company_id.id)
        return vals
