from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def create_variant_ids(self):
        single_variant_templates = self.filtered(
            lambda template: template._is_single_variant_attribute_template()
        )

        if single_variant_templates:
            single_variant_templates._sync_single_variant_attribute_values()

        return super(ProductTemplate, self).create_variant_ids()

    @api.multi
    def _is_single_variant_attribute_template(self):
        self.ensure_one()

        template = self.with_context(active_test=False)
        active_variants = template.product_variant_ids.filtered("active")

        if len(active_variants) != 1:
            return False

        for line in self.valid_product_template_attribute_line_wnva_ids:
            if len(line.value_ids) > 1:
                return False

        return True

    @api.multi
    def _sync_single_variant_attribute_values(self):
        for template in self:
            variant = template.with_context(active_test=False).product_variant_ids.filtered(
                "active"
            )

            value_ids = template.valid_product_template_attribute_line_wnva_ids.mapped(
                "value_ids"
            ).ids

            variant.write({
                "attribute_value_ids": [(6, 0, value_ids)],
            })

        self.invalidate_cache()
        self.env["product.product"].invalidate_cache()