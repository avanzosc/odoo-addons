# Copyright 2022 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    template = fields.Boolean(
        string='Template User', help="Template user to give internal access rights.")
