# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerCourseLevel(models.Model):
    _name = 'res.partner.course.level'
    _description = 'Course level'

    name = fields.Char(string='Course level', required=True)
