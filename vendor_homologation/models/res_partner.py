from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    food_homologated = fields.Boolean(
        string="Homologated for food",
        default=False,
    )
    food_homologation_first_date = fields.Date(
        string="First homologation date",
    )
    food_homologation_last_review_date = fields.Date(
        string="Last review date",
    )
