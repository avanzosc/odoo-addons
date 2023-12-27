# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductImportLine(models.Model):
    _inherit = "product.import.line"

    supplier_code = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    supplier_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    supplier_product_code = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    supplier_product_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    quantity = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    price = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    discount = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delay = fields.Integer(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    currency = fields.Char(
        string="Currency Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    date_start = fields.Date(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    date_end = fields.Date(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    import_supplierinfo_line_id = fields.Many2one(
        string="Supplierinfo Import Line",
        comodel_name="product.supplierinfo.import.line",
        readonly=True,
        copy=False,
    )

    def _create_supplierinfo_import_line(self):
        self.ensure_one()
        if (
            self.supplier_code or self.supplier_name
        ) and not self.import_supplierinfo_line_id:
            self.import_supplierinfo_line_id = self.env[
                "product.supplierinfo.import.line"
            ].create(
                {
                    "product_name": self.product_id.name,
                    "product_code": self.product_id.default_code,
                    "product_id": self.product_id.id,
                    "supplier_code": self.supplier_code,
                    "supplier_name": self.supplier_name,
                    "supplier_product_code": self.supplier_product_code,
                    "supplier_product_name": self.supplier_product_name,
                    "quantity": self.quantity,
                    "price": self.price,
                    "discount": self.discount,
                    "delay": self.delay,
                    "currency": self.currency,
                    "date_start": self.date_start,
                    "date_end": self.date_end,
                    "import_id": self.import_id.supplierinfo_import_id.id,
                }
            )
