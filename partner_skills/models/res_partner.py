# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_skill_ids = fields.One2many(
        comodel_name='hr.employee.skill', inverse_name='partner_id',
        string="Skills")
