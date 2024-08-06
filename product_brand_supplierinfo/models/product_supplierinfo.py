# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    product_brand_id = fields.Many2one(
        string="Brand", comodel_name="product.brand", copy=False
    )
    brand_code = fields.Char(
        string="Brand Code", related="product_brand_id.code", store=True, copy=False
    )
    brand_marking = fields.Char(
        string="Brand Marking",
        related="product_brand_id.marking",
        store=True,
        copy=False,
    )
