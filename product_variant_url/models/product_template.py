# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    external_url = fields.Char(
        compute="_compute_external_url",
        inverse="_inverse_external_url",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        for template, vals in zip(templates, vals_list, strict=False):
            related_vals = {}
            if vals.get("external_url"):
                related_vals["external_url"] = vals["external_url"]
            if related_vals:
                template.write(related_vals)
        return templates

    @api.depends("product_variant_ids", "product_variant_ids.external_url")
    def _compute_external_url(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.external_url = template.product_variant_ids.external_url
        for template in self - unique_variants:
            template.external_url = 0.0

    def _inverse_external_url(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.external_url = self.external_url
