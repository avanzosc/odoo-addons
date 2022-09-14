# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    country_id = fields.Many2one(
        string="Origin", comodel_name="res.country")
    global_gap = fields.Char(
        string="Global Gap")

    def _assign_production_lot(self, lot):
        result = super(StockMoveLine, self)._assign_production_lot(lot)
        if (self.picking_id.picking_type_id.code == "incoming" and
                self.country_id and self.global_gap):
            lot.write({"country_id": self.country_id.id,
                       "ref": self.global_gap})
        return result
