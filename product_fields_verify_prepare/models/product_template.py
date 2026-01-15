from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    verification_by = fields.Selection(
        [
            ("not_verified", "NOT VERIFIED"),
            ("sent", "SENT"),
            ("by_prototype", "BY PROTOTYPE"),
            ("by_age", "BY AGE"),
            ("by_plan", "BY PLAN"),
        ],
        string="Verification by",
        default="not_verified",
    )

    preparation = fields.Selection(
        [
            ("closed_box", "CLOSED BOX"),
            ("open_box", "OPEN BOX"),
            ("only_bodies", "ONLY BODIES"),
            ("only_lids", "ONLY LIDS"),
            ("only_fronts", "ONLY FRONTS"),
            ("no_preparation", "NO PREPARATION"),
        ],
        string="Preparation",
        default="no_preparation",
    )
