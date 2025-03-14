# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    in_qty = fields.Float(string="Incoming Qty", compute="_compute_in_qty")
    out_qty = fields.Float(string="Outgoing Qty", compute="_compute_out_qty")
    dif_qty = fields.Float(string="Difference", compute="_compute_dif_qty")

    def _compute_in_qty(self):
        for line in self:
            line.in_qty = 0
            if line.location_id and line.location_id.usage != "internal":
                line.in_qty = line.qty_done

    def _compute_out_qty(self):
        for line in self:
            line.out_qty = 0
            if line.location_dest_id and (line.location_dest_id.usage) != ("internal"):
                line.out_qty = line.qty_done * (-1)

    def _compute_dif_qty(self):
        for line in self:
            line.dif_qty = line.in_qty + line.out_qty
