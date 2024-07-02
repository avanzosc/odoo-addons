# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def create(self, values):
        employee = super().create(values)
        if employee.user_id:
            employee.user_id.catch_user_languages()
        return employee

    def write(self, values):
        result = super().write(values)
        if "user_id" in values:
            for employee in self:
                employee.user_id.catch_user_languages()
        return result
