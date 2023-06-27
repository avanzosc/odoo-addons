# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductImportLine(models.Model):
    _inherit = "product.import.line"

    packaging_name = fields.Char(
        string="Packaging Name",
        )
    packaging_barcode = fields.Char(
        string="Packaging Barcode",
        )
    packaging_quantity = fields.Float(
        string="Quantity",
        )
    max_weight = fields.Float(
        string="Max Weight",
        )
    weight = fields.Float(
        string="Weight",
        )
    length = fields.Float(
        string="Length",
        )
    width = fields.Float(
        string="Width",
        )
    height = fields.Float(
        string="Height",
        )
    import_packaging_line_id = fields.Many2one(
        string="Packaging Impor Line",
        comodel_name="product.packaging.import.line",
        readonly=True,
        )
