# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerType(models.Model):
    _name = 'res.partner.type'
    _description = 'Partner types'

    name = fields.Char(string="Description")
    is_school = fields.Boolean(string='Is one school?', default=False)
