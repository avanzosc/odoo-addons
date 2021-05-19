# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerEmploymentSituation(models.Model):
    _name = 'res.partner.employment.situation'
    _description = 'Employment situation'

    name = fields.Char(string='Employment situation', required=True)
