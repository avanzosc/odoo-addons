from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    series_id = fields.Many2one("product.series", string="Series")
    model_id = fields.Many2one("product.model", string="Model")
    application_id = fields.Many2one("product.application", string="Application")
    family_id = fields.Many2one("product.family", string="Family")
    packaging_type = fields.Selection(
        [("industrial", "Industrial"), ("standard", "Standard"), ("retail", "Retail")],
        string="Packaging Type",
    )
