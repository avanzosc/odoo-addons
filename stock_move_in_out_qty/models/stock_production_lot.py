# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    in_qty = fields.Float(string="Incoming Qty", compute="_compute_in_qty")
    out_qty = fields.Float(string="Outgoing Qty", compute="_compute_out_qty")
    dif_qty = fields.Float(string="Difference", compute="_compute_dif_qty")
    move_line_ids = fields.One2many(
        string="Move Lines", comodel_name="stock.move.line", inverse_name="lot_id"
    )

    def _compute_in_qty(self):
        for line in self:
            line.in_qty = 0
            lines = line.move_line_ids.filtered(lambda c: c.state == "done")
            if lines:
                line.in_qty = sum(lines.mapped("in_qty"))

    def _compute_out_qty(self):
        for line in self:
            line.out_qty = 0
            lines = line.move_line_ids.filtered(lambda c: c.state == "done")
            if lines:
                line.out_qty = sum(lines.mapped("out_qty"))

    def _compute_dif_qty(self):
        for line in self:
            line.dif_qty = 0
            lines = line.move_line_ids.filtered(lambda c: c.state == "done")
            if lines:
                line.dif_qty = sum(lines.mapped("dif_qty"))
