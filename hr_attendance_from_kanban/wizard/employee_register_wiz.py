# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models


class EmployeeRegisterWiz(models.TransientModel):
    _name = 'employee.register.wiz'

    register_pass = fields.Char()

    @api.multi
    def sign_in_employee(self):
        employee = self.env['hr.employee'].browse(
            self.env.context.get('active_id'))
        if not employee.user_id:
            raise exceptions.Warning(_("This employee has no user assigned"))
        else:
            if self.register_pass == employee.user_id.register_pass:
                return employee.attendance_action_change()
            else:
                raise exceptions.Warning(_("Incorrect password"))
