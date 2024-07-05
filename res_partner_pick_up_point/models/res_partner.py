from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    pick_up_point_id = fields.Many2one(
        "Pick Up Point",
        "res.partner",
    )
