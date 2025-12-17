from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    production_verification_by = fields.Selection(
        related="sale_line_id.verification_by",
        string="Verification by",
        readonly=False,
    )
    production_preparation = fields.Selection(
        related="sale_line_id.preparation",
        string="Preparation",
        readonly=False,
    )
