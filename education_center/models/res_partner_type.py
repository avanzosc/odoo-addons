# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerType(models.Model):
    _inherit = 'res.partner.type'

    is_education_center = fields.Boolean(
        string='Is education center?', default=False)
