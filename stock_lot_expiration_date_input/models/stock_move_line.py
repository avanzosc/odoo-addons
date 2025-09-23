# Copyright 2025 Ane Gurruchaga- AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    manual_expiration_date = fields.Datetime(
        string="Expiration Date Manual",
    )

    def _assign_production_lot(self, lot):
        res = super()._assign_production_lot(lot)
        for move_line in self:
            if move_line.manual_expiration_date:
                lot.expiration_date = move_line.manual_expiration_date
        return res
