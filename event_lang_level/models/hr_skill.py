# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HrSkill(models.Model):
    _inherit = 'hr.skill'

    code = fields.Char(string='Code')
