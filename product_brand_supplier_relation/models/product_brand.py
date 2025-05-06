# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    suppliers_ids = fields.One2many(
        string="Suppliers",
        comodel_name="product.brand.supplier.relation",
        inverse_name="product_brand_id",
    )
