# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_old_reference = fields.Char(
        string="Old reference",
        store=True,
        copy=False,
        compute="_compute_product_old_refence",
        inverse="_set_product_old_reference",
    )

    @api.depends("product_variant_ids", "product_variant_ids.product_old_reference")
    def _compute_product_old_refence(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.product_old_reference = (
                template.product_variant_ids.product_old_reference
            )
        for template in self - unique_variants:
            template.product_old_reference = False

    def _set_product_old_reference(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.product_old_reference = (
                    template.product_old_reference
                )
