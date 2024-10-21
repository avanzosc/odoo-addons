from odoo import fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    users = fields.Many2many(copy=False)
    name = fields.Char(copy=False)
