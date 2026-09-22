# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    in_qty = fields.Float(
        string="Incoming Qty", compute="_compute_in_out_qty", store=True
    )
    out_qty = fields.Float(
        string="Outgoing Qty", compute="_compute_in_out_qty", store=True
    )
    dif_qty = fields.Float(
        string="Difference", compute="_compute_in_out_qty", store=True
    )
    move_line_ids = fields.One2many(
        string="Move Lines", comodel_name="stock.move.line", inverse_name="lot_id"
    )

    @api.depends(
        "move_line_ids",
        "move_line_ids.in_qty",
        "move_line_ids.out_qty",
        "move_line_ids.state",
    )
    def _compute_in_out_qty(self):
        for lot in self:
            lot.in_qty = 0
            lot.out_qty = 0
            done_lines = lot.move_line_ids.filtered(lambda c: c.state == "done")
            if done_lines:
                lot.in_qty = sum(done_lines.mapped("in_qty"))
                lot.out_qty = sum(done_lines.mapped("out_qty"))
            lot.dif_qty = lot.in_qty + lot.out_qty
