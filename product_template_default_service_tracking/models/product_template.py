from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    service_tracking = fields.Selection(
        [
            ("no", "Don't create task"),
            ("task_global_project", "Create a task in an existing project"),
            ("task_in_project", "Create a task in sales order's project"),
            ("project_only", "Create a new project but no task"),
        ],
        default="project_only",
    )
