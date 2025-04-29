from odoo import api, models, fields
from odoo.tools import pycompat


class ProductProduct(models.Model):
    _inherit = 'product.product'

    external_url = fields.Char("External URL")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    external_url = fields.Char(
        string="External URL",
        compute="_compute_external_url",
        inverse="_set_external_url",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Set given values to first variant after creation"""
        templates = super().create(vals_list)
        for template, vals in pycompat.izip(templates, vals_list):
            related_vals = {}
            if vals.get("external_url"):
                related_vals["external_url"] = vals["external_url"]
            if related_vals:
                template.write(related_vals)
        return templates

    @api.depends('product_variant_ids', 'product_variant_ids.external_url')
    def _compute_external_url(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.external_url = template.product_variant_ids.external_url
        for template in (self - unique_variants):
            template.external_url = 0.0

    @api.one
    def _set_external_url(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.external_url = self.external_url
