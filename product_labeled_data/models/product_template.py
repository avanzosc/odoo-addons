# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    labeled_length = fields.Char(
        string="Length",
        compute="_compute_labeled_length",
        inverse="_set_labeled_length",
        store=True,
        copy=False,
    )
    description_label_es = fields.Char(
        string="Description label (es)",
        compute="_compute_description_label_es",
        inverse="_set_description_label_es",
        store=True,
        copy=False,
    )
    description_label_fr = fields.Char(
        string="Description label (fr)",
        compute="_compute_description_label_fr",
        inverse="_set_description_label_fr",
        store=True,
        copy=False,
    )
    description_label_en = fields.Char(
        string="Description label (en)",
        compute="_compute_description_label_en",
        inverse="_set_description_label_en",
        store=True,
        copy=False,
    )
    labeled_finished_code = fields.Char(
        string="Finished code",
        compute="_compute_labeled_finished_code",
        inverse="_set_labeled_finished_code",
        store=True,
        copy=False,
    )
    labeled_color_es = fields.Char(
        string="Color (es)",
        compute="_compute_labeled_color_es",
        inverse="_set_labeled_color_es",
        store=True,
        copy=False,
    )
    labeled_color_fr = fields.Char(
        string="Color (fr)",
        compute="_compute_labeled_color_fr",
        inverse="_set_labeled_color_fr",
        store=True,
        copy=False,
    )
    labeled_color_en = fields.Char(
        string="Color (en)",
        compute="_compute_labeled_color_en",
        inverse="_set_labeled_color_en",
        store=True,
        copy=False,
    )

    @api.depends("product_variant_ids", "product_variant_ids.labeled_length")
    def _compute_labeled_length(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.labeled_length = template.product_variant_ids.labeled_length
        for template in self - unique_variants:
            template.labeled_length = ""

    def _set_labeled_length(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.labeled_length = template.labeled_length

    @api.depends("product_variant_ids", "product_variant_ids.description_label_es")
    def _compute_description_label_es(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.description_label_es = (
                template.product_variant_ids.description_label_es
            )
        for template in self - unique_variants:
            template.description_label_es = ""

    def _set_description_label_es(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.description_label_es = (
                    template.description_label_es
                )

    @api.depends("product_variant_ids", "product_variant_ids.description_label_fr")
    def _compute_description_label_fr(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.description_label_fr = (
                template.product_variant_ids.description_label_fr
            )
        for template in self - unique_variants:
            template.description_label_fr = ""

    def _set_description_label_fr(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.description_label_fr = (
                    template.description_label_fr
                )

    @api.depends("product_variant_ids", "product_variant_ids.description_label_en")
    def _compute_description_label_en(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.description_label_en = (
                template.product_variant_ids.description_label_en
            )
        for template in self - unique_variants:
            template.description_label_en = ""

    def _set_description_label_en(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.description_label_en = (
                    template.description_label_en
                )

    @api.depends("product_variant_ids", "product_variant_ids.labeled_finished_code")
    def _compute_labeled_finished_code(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.labeled_finished_code = (
                template.product_variant_ids.labeled_finished_code
            )
        for template in self - unique_variants:
            template.labeled_finished_code = ""

    def _set_labeled_finished_code(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.labeled_finished_code = (
                    template.labeled_finished_code
                )

    @api.depends("product_variant_ids", "product_variant_ids.labeled_color_es")
    def _compute_labeled_color_es(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.labeled_color_es = template.product_variant_ids.labeled_color_es
        for template in self - unique_variants:
            template.labeled_color_es = ""

    def _set_labeled_color_es(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.labeled_color_es = (
                    template.labeled_color_es
                )

    @api.depends("product_variant_ids", "product_variant_ids.labeled_color_fr")
    def _compute_labeled_color_fr(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.labeled_color_fr = template.product_variant_ids.labeled_color_fr
        for template in self - unique_variants:
            template.labeled_color_fr = ""

    def _set_labeled_color_fr(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.labeled_color_fr = (
                    template.labeled_color_fr
                )

    @api.depends("product_variant_ids", "product_variant_ids.labeled_color_en")
    def _compute_labeled_color_en(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.labeled_color_en = template.product_variant_ids.labeled_color_en
        for template in self - unique_variants:
            template.labeled_color_en = ""

    def _set_labeled_color_en(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.labeled_color_en = (
                    template.labeled_color_en
                )

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if vals.get("labeled_length"):
                related_vals["labeled_length"] = vals["labeled_length"]
            if vals.get("description_label_es"):
                related_vals["description_label_es"] = vals["description_label_es"]
            if vals.get("description_label_fr"):
                related_vals["description_label_fr"] = vals["description_label_fr"]
            if vals.get("description_label_en"):
                related_vals["description_label_en"] = vals["description_label_en"]
            if vals.get("labeled_finished_code"):
                related_vals["labeled_finished_code"] = vals["labeled_finished_code"]
            if vals.get("labeled_color_es"):
                related_vals["labeled_color_es"] = vals["labeled_color_es"]
            if vals.get("labeled_color_fr"):
                related_vals["labeled_color_fr"] = vals["labeled_color_fr"]
            if vals.get("labeled_color_en"):
                related_vals["labeled_color_en"] = vals["labeled_color_en"]
            if related_vals:
                template.write(related_vals)
        return templates
