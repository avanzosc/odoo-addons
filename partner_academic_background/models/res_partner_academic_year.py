# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerAcademicYear(models.Model):
    _name = 'res.partner.academic.year'
    _description = 'Academic year'

    name = fields.Char(string='Academic year', required=True)
