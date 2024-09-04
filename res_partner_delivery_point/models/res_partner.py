from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_point = fields.Many2one(
        "res.partner",
        "Pick Up Point",
    )
