# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ProductBrandSupplierRelation(models.Model):
    _name = "product.brand.supplier.relation"
    _description = "Product Brand Supplier Relation"

    supplier_id = fields.Many2one(
        string="Supplier", comodel_name="res.partner", required=True
    )
    product_brand_id = fields.Many2one(
        string="Product Brand", comodel_name="product.brand", required=True
    )

    _sql_constraints = [
        (
            "unique_supplier_product_brand",
            "unique(supplier_id,product_brand_id)",
            _("There is already a record for this supplier and product brand"),
        )
    ]
