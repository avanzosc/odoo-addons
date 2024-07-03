# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductImportLine(models.Model):
    _inherit = "product.import.line"

    packaging_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    packaging_barcode = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    packaging_quantity = fields.Float(
        string="Quantity",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    max_weight = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    weight = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    packaging_length = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    width = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    height = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    import_packaging_line_id = fields.Many2one(
        string="Packaging Import Line",
        comodel_name="product.packaging.import.line",
        readonly=True,
        copy=False,
    )

    def _create_packaging_import_line(self):
        self.ensure_one()
        if self.packaging_name and not self.import_packaging_line_id:
            self.import_packaging_line_id = self.env[
                "product.packaging.import.line"
            ].create(
                {
                    "product_name": self.product_id.name,
                    "product_default_code": self.product_id.default_code,
                    "product_id": self.product_id.id,
                    "packaging_name": self.packaging_name,
                    "barcode": self.packaging_barcode,
                    "quantity": self.packaging_quantity,
                    "max_weight": self.max_weight,
                    "weight": self.weight,
                    "packaging_length": self.packaging_length,
                    "width": self.width,
                    "height": self.height,
                    "import_id": self.import_id.packaging_import_id.id,
                }
            )
