# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    download_unit = fields.Integer(
        string="Units", compute="_compute_download_unit", store=True
    )

    @api.depends("move_line_ids", "move_line_ids.download_unit")
    def _compute_download_unit(self):
        for line in self:
            line.download_unit = 0
            if line.move_line_ids:
                line.download_unit = sum(
                    line.move_line_ids.filtered(lambda c: c.state == "done").mapped(
                        "download_unit"
                    )
                )
