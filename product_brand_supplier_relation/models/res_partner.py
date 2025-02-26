# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    product_brand_ids = fields.One2many(
        string="Brands",
        comodel_name="product.brand.supplier.relation",
        inverse_name="supplier_id",
    )
