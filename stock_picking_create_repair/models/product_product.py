# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    default_product_manufacturing_operations = fields.Boolean(
        string="Default product for manufacturing operations", default=False,
        copy=False)

    @api.model
    def create(self, vals):
        if "product_tmpl_id" in vals and vals.get("product_tmpl_id", False):
            template = self.env["product.template"].browse(
                vals.get("product_tmpl_id"))
            if template.product_variant_count == 0:
                vals.update({
                    "default_product_manufacturing_operations":
                    template.default_product_manufacturing_operations})
        product = super(ProductProduct, self).create(vals)
        if "product_tmpl_id" not in vals:
            if product.product_tmpl_id.product_variant_count == 1:
                product.product_tmpl_id.write({
                    "default_product_manufacturing_operations":
                    product.default_product_manufacturing_operations})
        return product

    def write(self, vals):
        result = super(ProductProduct, self).write(vals)
        if ("no_update_template" not in self.env.context and
                "default_product_manufacturing_operations" in vals):
            for product in self:
                if product.product_tmpl_id.product_variant_count == 1:
                    template = product.product_tmpl_id
                    template_vals = {
                        "default_product_manufacturing_operations":
                        product.default_product_manufacturing_operations}
                    template.with_context(
                        no_update_product=True).write(template_vals)
        return result
