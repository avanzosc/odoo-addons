# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    def _default_product_tmpl_id_domain(self):
        if "default_product_tmpl_id" in self.env.context:
            return self.env["product.template"].browse(
                self.env.context.get("default_product_tmpl_id")
            )
        if self.env.context.get("model") == "product.template":
            return self.env["product.template"].browse(
                self.env.context.get("active_id")
            )
        if self.env.context.get("model") == "product.product":
            product = self.env["product.product"].browse(
                self.env.context.get("active_id")
            )
            return product.product_tmpl_id

    product_brand_id = fields.Many2one(
        string="Brand", comodel_name="product.brand", copy=False
    )
    brand_code = fields.Char(copy=False)
    brand_marking = fields.Char(
        string="Brand Marking",
        related="product_brand_id.marking",
        store=True,
        copy=False,
    )
    brand_product_id = fields.Many2one(
        string="Product Brand", comodel_name="brand.product", copy=False
    )
    product_tmpl_id_domain = fields.Many2one(
        string="Product Template Domain",
        comodel_name="product.template",
        default=_default_product_tmpl_id_domain,
    )

    @api.onchange("brand_product_id")
    def onchange_brand_product_id(self):
        if self.brand_product_id:
            self.brand_code = self.brand_product_id.brand_code
            if self.brand_product_id.brand_id:
                self.product_brand_id = self.brand_product_id.brand_id.id
