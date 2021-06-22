# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _compute_is_manager(self):
        manager = self.env.ref('hr.group_hr_manager')
        for employee in self:
            employee.is_manager = False
            if employee.user_id in manager.users:
                employee.is_manager = True

    personal_private_email = fields.Char(string='Personal private email')
    is_manager = fields.Boolean(
        string='Is manager', compute='_compute_is_manager')
