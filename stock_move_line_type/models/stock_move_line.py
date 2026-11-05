# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    move_line_type = fields.Selection(
        selection=[
            ("incoming", "Incoming"),
            ("outgoing", "Outgoing"),
            ("expired", "Expired"),
            ("internal", "Internal"),
            ("other", "Other"),
        ],
        compute="_compute_move_line_type",
        store=True,
    )

    @api.depends(
        "location_id.usage",
        "location_dest_id.usage",
        "location_dest_id.scrap_location",
    )
    def _compute_move_line_type(self):
        for record in self:
            src = record.location_id.usage
            dst = record.location_dest_id.usage
            scrap = record.location_dest_id.scrap_location
            if src != "internal" and dst == "internal":
                record.move_line_type = "incoming"
            elif src == "internal" and dst != "internal" and scrap:
                record.move_line_type = "expired"
            elif src == "internal" and dst != "internal":
                record.move_line_type = "outgoing"
            elif src == "internal" and dst == "internal":
                record.move_line_type = "internal"
            else:
                record.move_line_type = "other"
