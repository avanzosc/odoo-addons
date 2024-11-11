from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    origin_declaration = fields.Html()
