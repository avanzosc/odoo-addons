# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    max_weight = fields.Float(
        "Maximum Weight", related='packaging_id.max_weight', store=True)
    weight_uom_name = fields.Char(
        string="Weight unit of measure label",
        related="packaging_id.weight_uom_name", store=True)
    height = fields.Float(string="Height")
    width = fields.Float(string="Width")
    packaging_length = fields.Float(string="Length")
    length_uom_name = fields.Char(
        string="Length unit of measure label",
        related="packaging_id.length_uom_name", store=True)

    @api.onchange('packaging_id')
    def onchange_dimension(self):
        self.height = self.packaging_id.height
        self.width = self.packaging_id.width
        self.packaging_length = self.packaging_id.packaging_length
