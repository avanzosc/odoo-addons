# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductImportLine(models.Model):
    _inherit = "product.import.line"

    supplier_code = fields.Char(
        string="Supplier Code",
        )
    supplier_name = fields.Char(
        string="Supplier Name",
        )
    supplier_product_code = fields.Char(
        string="Supplier Product Code",
        )
    supplier_product_name = fields.Char(
        string="Supplier Product Name",
        )
    quantity = fields.Float(
        string="Quantity",
        )
    price = fields.Float(
        string="Price",
        )
    discount = fields.Float(
        string="Discount",
        )
    delay = fields.Integer(
        string="Delay",
        )
    currency = fields.Char(
        string="Currency Name",
        )
    date_start = fields.Date(
        string="Date Start",
        )
    date_end = fields.Date(
        string="Date End",
        )
    import_supplierinfo_line_id = fields.Many2one(
        string="Supplierinfo Impor Line",
        comodel_name="product.supplierinfo.import.line",
        readonly=True,
        )
