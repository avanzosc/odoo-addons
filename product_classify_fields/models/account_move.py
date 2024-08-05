from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    product_series_id = fields.Many2one(
        "product.series",
        related="invoice_line_ids.product_series_id",
        string="Series",
        store=True,
        readonly=True,
    )
    product_model_id = fields.Many2one(
        "product.model",
        related="invoice_line_ids.product_model_id",
        string="Model",
        store=True,
        readonly=True,
    )
    product_family_id = fields.Many2one(
        "product.family",
        related="invoice_line_ids.product_family_id",
        string="Family",
        store=True,
        readonly=True,
    )
    product_application_id = fields.Many2one(
        "product.application",
        related="invoice_line_ids.product_application_id",
        string="Application",
        store=True,
        readonly=True,
    )
    product_color_id = fields.Many2one(
        "product.color",
        related="invoice_line_ids.product_color_id",
        string="Color",
        store=True,
        readonly=True,
    )
    product_packaging_type = fields.Selection(
        related="invoice_line_ids.product_packaging_type",
        string="Packaging Type",
        store=True,
        readonly=True,
    )
