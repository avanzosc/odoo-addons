# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_grade_id = fields.Many2one(
        string="Grade",
        comodel_name="product.template.attribute.value",
        compute="_compute_product_grade_id",
        copy=False,
        store=True,
    )
    product_thickness_id = fields.Many2one(
        string="Thickness",
        comodel_name="product.template.attribute.value",
        compute="_compute_product_thickness_id",
        copy=False,
        store=True,
    )

    @api.depends("product_template_attribute_value_ids")
    def _compute_product_grade_id(self):
        grade_att = self.env["product.attribute"].search(
            [("name", "=", "GRADE")], limit=1
        )
        for record in self:
            grade = record.product_template_attribute_value_ids.filtered(
                lambda v: v.attribute_id == grade_att
            )
            record.product_grade_id = grade or False

    @api.depends("product_template_attribute_value_ids")
    def _compute_product_thickness_id(self):
        thickness_att = self.env["product.attribute"].search(
            [("name", "=", "THICKNESS")], limit=1
        )
        for record in self:
            thickness = record.product_template_attribute_value_ids.filtered(
                lambda v: v.attribute_id == thickness_att
            )
            record.product_thickness_id = thickness or False
