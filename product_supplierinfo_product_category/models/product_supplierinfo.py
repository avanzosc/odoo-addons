# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    product_categ_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        related="product_tmpl_id.categ_id",
        store=True,
        copy=False,
    )
