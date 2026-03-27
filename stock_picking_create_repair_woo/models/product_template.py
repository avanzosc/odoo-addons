# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    generic_repair_product = fields.Boolean(
        string="Generic Repair Product",
        default=False,
        copy=False,
        help="It's a generic repair product?",
    )

    def write(self, vals):
        result = super().write(vals)
        if (
            "no_update_product" not in self.env.context
            and "generic_repair_product" in vals
        ):
            for template in self:
                if template.product_variant_count == 1:
                    variant = template.product_variant_ids[0]
                    variant_vals = {
                        "generic_repair_product": (template.generic_repair_product)
                    }
                    variant.with_context(no_update_template=True).write(variant_vals)
        return result

    @api.constrains("generic_repair_product")
    def _check_generic_repair_product(self):
        for template in self.filtered(lambda x: x.generic_repair_product):
            cond = [("id", "!=", template.id), ("generic_repair_product", "=", True)]
            other_template = self.env["product.template"].search(cond, limit=1)
            if other_template:
                error = _(
                    "The product: %(product)s it is already marked as "
                    "generic repair product."
                ) % {"product": other_template.name}
                raise ValidationError(error)
