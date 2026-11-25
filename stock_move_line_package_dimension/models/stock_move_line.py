# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    height = fields.Float(string="Height", related="packaging_id.height", store=True)
    width = fields.Float(string="Width", related="packaging_id.width", store=True)
    packaging_length = fields.Float(
        string="Packaging Length", related="packaging_id.packaging_length", store=True
    )
    length_uom_name = fields.Char(
        string="Length UoM", related="packaging_id.length_uom_id.name"
    )
    volume = fields.Float(compute="_compute_volume", store=True)
    volume_uom_name = fields.Char(
        string="Volume UoM", related="packaging_id.volume_uom_id.name"
    )

    @api.depends(
        "packaging_id",
        "packaging_id.packaging_length",
        "packaging_id.height",
        "packaging_id.width",
        "packaging_id.length_uom_id",
        "packaging_id.volume_uom_id",
    )
    def _compute_volume(self):
        for line in self:
            line.volume = line.packaging_id.volume if line.packaging_id else 0.0
