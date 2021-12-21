# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    max_weight = fields.Float(
        "Maximum Weight", related='packaging_id.max_weight', store=True)
    weight_uom_name = fields.Char(
        string="Weight unit of measure label",
        related="packaging_id.weight_uom_name", store=True)
    height = fields.Float(
        string="Height", related='packaging_id.height', store=True)
    width = fields.Float(
        string="Width", related='packaging_id.width', store=True)
    packaging_length = fields.Float(
        string="Length", related='packaging_id.packaging_length', store=True)
    length_uom_name = fields.Char(
        string="Length unit of measure label",
        related="packaging_id.length_uom_name", store=True)
