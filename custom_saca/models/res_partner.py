# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    farm_numexp = fields.Char(string='Rega')
    ates = fields.Char(string='Ates')
    distance = fields.Float(string='Distance')
