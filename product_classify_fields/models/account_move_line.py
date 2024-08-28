from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_template_id = fields.Many2one(
        "product.template",
        related="product_id.product_tmpl_id",
        string="Product Template",
        store=True,
    )

    product_series_id = fields.Many2one(
        "product.series",
        related="product_template_id.series_id",
        string="Series",
        store=True,
    )
    product_model_id = fields.Many2one(
        "product.model",
        related="product_template_id.model_id",
        string="Model",
        store=True,
    )
    product_family_id = fields.Many2one(
        "product.family",
        related="product_template_id.family_id",
        string="Family",
        store=True,
    )
    product_application_id = fields.Many2one(
        "product.application",
        related="product_template_id.application_id",
        string="Application",
        store=True,
    )
    product_color_id = fields.Many2one(
        "product.color",
        related="product_template_id.color_id",
        string="Color",
        store=True,
    )
    product_packaging_type = fields.Selection(
        related="product_template_id.packaging_type",
        string="Packaging Type",
        store=True,
    )
