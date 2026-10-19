# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    product_brand_id = fields.Many2one(
        string="Brand", comodel_name="product.brand", copy=False
    )

    brand_code = fields.Char(copy=False)

    brand_product_id = fields.Many2one(
        string="Homologation", comodel_name="brand.product", copy=False
    )

    @api.onchange("brand_product_id")
    def onchange_brand_product_id(self):
        if self.brand_product_id:
            self.brand_code = self.brand_product_id.brand_code
            if self.brand_product_id.brand_id:
                self.product_brand_id = self.brand_product_id.brand_id.id
