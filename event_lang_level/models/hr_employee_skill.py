# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class HrEmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    @api.model
    def create(self, values):
        employee_skill = super(HrEmployeeSkill, self).create(values)
        if (employee_skill.skill_type_id and employee_skill.employee_id and
            employee_skill.skill_type_id.skill_language and
                employee_skill.employee_id.user_id):
            employee_skill.employee_id.user_id.catch_user_languages()
        return employee_skill

    def write(self, values):
        result = super(HrEmployeeSkill, self).write(values)
        if "skill_type_id" in values:
            for employee_skill in self:
                if (employee_skill.skill_type_id and
                    employee_skill.employee_id and
                    employee_skill.skill_type_id.skill_language and
                        employee_skill.employee_id.user_id):
                    employee_skill.employee_id.user_id.catch_user_languages()
        return result
