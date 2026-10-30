# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends(
        "attribute_line_ids.attribute_id.hide_in_configuration",
        "attribute_line_ids.attribute_id.create_variant",
    )
    def _compute_valid_product_template_attribute_line_ids(self):
        res = super()._compute_valid_product_template_attribute_line_ids()
        for template in self:
            template.valid_product_template_attribute_line_ids = (
                template.valid_product_template_attribute_line_ids.filtered(
                    lambda line: not line._is_hidden_in_configuration()
                )
            )
        return res

    @api.depends("attribute_line_ids.attribute_id.hide_in_configuration")
    def _compute_has_configurable_attributes(self):
        return super()._compute_has_configurable_attributes()
