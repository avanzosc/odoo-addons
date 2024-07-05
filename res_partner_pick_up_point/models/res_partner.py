from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    pick_up_point_id = fields.Many2one(
        "res.partner",
        "Pick Up Point",
    )
