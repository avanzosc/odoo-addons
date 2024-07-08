# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    in_qty = fields.Float(string="Incoming Qty", compute="_compute_in_qty", store=True)
    out_qty = fields.Float(
        string="Outgoing Qty", compute="_compute_out_qty", store=True
    )
    dif_qty = fields.Float(string="Difference", compute="_compute_dif_qty", store=True)
    move_line_ids = fields.One2many(
        string="Move Lines", comodel_name="stock.move.line", inverse_name="lot_id"
    )

    @api.depends("move_line_ids", "move_line_ids.in_qty", "move_line_ids.state")
    def _compute_in_qty(self):
        for line in self:
            line.in_qty = 0
            lines = line.move_line_ids.filtered(lambda c: c.state == "done")
            if lines:
                line.in_qty = sum(lines.mapped("in_qty"))

    @api.depends("move_line_ids", "move_line_ids.out_qty", "move_line_ids.state")
    def _compute_out_qty(self):
        for line in self:
            line.out_qty = 0
            lines = line.move_line_ids.filtered(lambda c: c.state == "done")
            if lines:
                line.out_qty = sum(lines.mapped("out_qty"))

    @api.depends("move_line_ids", "move_line_ids.dif_qty", "move_line_ids.state")
    def _compute_dif_qty(self):
        for line in self:
            line.dif_qty = 0
            lines = line.move_line_ids.filtered(lambda c: c.state == "done")
            if lines:
                line.dif_qty = sum(lines.mapped("dif_qty"))
