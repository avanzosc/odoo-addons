# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

STATE_SELECTION = [
    ("clearance", "Clearance"),
    ("stock", "Stock"),
    ("mto", "Make To Order"),
    ("sample", "Sample"),
    ("discontinued", "Discontinued"),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    state = fields.Selection(
        selection=STATE_SELECTION,
        string="Status",
    )
    shipping_length = fields.Float(string="Length")

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        if "no_update_template_state" not in self.env.context:
            for template in templates:
                for variant in template.product_variant_ids:
                    if template.state != variant.state:
                        variant.with_context(no_update_product_state=True).write(
                            {"state": template.state}
                        )
        return templates

    def write(self, vals):
        result = super().write(vals)
        if (
            "state" in vals
            and vals.get("state", False)
            and "no_update_template_state" not in self.env.context
        ):
            for template in self:
                for variant in template.product_variant_ids:
                    if template.state != variant.state:
                        variant.with_context(no_update_product_state=True).write(
                            {"state": template.state}
                        )
        if "no_update_product" not in self.env.context and "shipping_length" in vals:
            for template in self:
                if template.product_variant_count == 1:
                    variant = template.product_variant_ids[0]
                    variant_vals = {"shipping_length": template.shipping_length}
                    variant.with_context(no_update_template=True).write(variant_vals)
        return result
