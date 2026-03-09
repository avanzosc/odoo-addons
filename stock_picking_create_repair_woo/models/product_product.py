# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    generic_repair_product = fields.Boolean(
        string="Generic Repair Product",
        default=False,
        copy=False,
        help="It's a generic repair product?",
    )

    @api.model
    def create(self, vals):
        if "product_tmpl_id" in vals and vals.get("product_tmpl_id", False):
            template = self.env["product.template"].browse(vals.get("product_tmpl_id"))
            if template.product_variant_count == 0:
                vals.update(
                    {"generic_repair_product": (template.generic_repair_product)}
                )
        product = super().create(vals)
        if "product_tmpl_id" not in vals:
            if product.product_tmpl_id.product_variant_count == 1:
                product.product_tmpl_id.write(
                    {"generic_repair_product": (product.generic_repair_product)}
                )
        return product

    def write(self, vals):
        result = super().write(vals)
        if (
            "no_update_template" not in self.env.context
            and "generic_repair_product" in vals
        ):
            for product in self:
                if product.product_tmpl_id.product_variant_count == 1:
                    template = product.product_tmpl_id
                    template_vals = {
                        "generic_repair_product": (product.generic_repair_product)
                    }
                    template.with_context(no_update_product=True).write(template_vals)
        return result

    @api.constrains("generic_repair_product")
    def _check_generic_repair_product(self):
        for product in self.filtered(lambda x: x.generic_repair_product):
            cond = [("id", "!=", product.id), ("generic_repair_product", "=", True)]
            other_product = self.env["product.product"].search(cond, limit=1)
            if other_product:
                error = _(
                    "The product variant: %(product)s it is already marked as "
                    "generic repair product."
                ) % {"product": other_product.name}
                raise ValidationError(error)
