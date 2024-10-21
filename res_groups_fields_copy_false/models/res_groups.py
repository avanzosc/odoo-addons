# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    name = fields.Char(copy=False)
    users = fields.Many2many(copy=False)
