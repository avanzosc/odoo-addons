# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_repair = fields.Boolean(
        string="Is repair", default=False, copy=False)
    default_product_manufacturing_operations = fields.Boolean(
        string="Default product for manufacturing operations", default=False,
        copy=False)

    @api.onchange('type')
    def _onchange_type(self):
        result = super(ProductTemplate, self)._onchange_type()
        for template in self:
            if template.type != "service":
                template.is_repair = False
        return result

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        return product

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        if ("no_update_product" not in self.env.context and
                "default_product_manufacturing_operations" in vals):
            for template in self:
                if template.product_variant_count == 1:
                    variant = template.product_variant_ids[0]
                    variant_vals = {
                        "default_product_manufacturing_operations":
                        template.default_product_manufacturing_operations}
                    variant.with_context(
                        no_update_template=True).write(variant_vals)
        return result
