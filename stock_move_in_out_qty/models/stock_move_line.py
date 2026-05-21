# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    in_qty = fields.Float(
        string="Incoming Qty", compute="_compute_in_out_qty", store=True
    )
    out_qty = fields.Float(
        string="Outgoing Qty", compute="_compute_in_out_qty", store=True
    )
    dif_qty = fields.Float(
        string="Difference", compute="_compute_in_out_qty", store=True
    )

    @api.depends(
        "quantity",
        "location_id",
        "location_id.usage",
        "location_dest_id",
        "location_dest_id.usage",
    )
    def _compute_in_out_qty(self):
        for line in self:
            line.in_qty = 0
            line.out_qty = 0

            if not (line.location_id and line.location_dest_id):
                line.dif_qty = 0
                continue

            src_usage = line.location_id.usage
            dest_usage = line.location_dest_id.usage

            if src_usage == "internal" and dest_usage == "internal":
                line.in_qty = line.quantity
                line.out_qty = -line.quantity

            elif src_usage != "internal" and dest_usage == "internal":
                line.in_qty = line.quantity

            elif src_usage == "internal" and dest_usage != "internal":
                line.out_qty = -line.quantity

            line.dif_qty = line.in_qty + line.out_qty
