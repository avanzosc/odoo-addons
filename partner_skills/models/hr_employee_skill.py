# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    partner_id = fields.Many2one(
        string='Partner', comodel_name='res.partner')
    employee_id = fields.Many2one(required=False)

    @api.model
    def create(self, values):
        if 'partner_id' not in values and 'employee_id' not in values:
            raise ValidationError(
                _("You must introduce the partner or the employee."))
        if 'partner_id' in values and values.get('partner_id', False):
            partner = self.env['res.partner'].browse(values.get('partner_id'))
            cond = [('partner_id', '=', partner.id)]
            user = self.env['res.users'].search(cond, limit=1)
            if user:
                cond = [('user_id', '=', user.id)]
                employee = self.env['hr.employee'].search(cond, limit=1)
                if employee:
                    values['employee_id'] = employee.id
        else:
            if 'employee_id' in values and values.get('employee_id', False):
                employee = self.env['hr.employee'].browse(
                    values.get('employee_id'))
                if employee and employee.user_id.partner_id:
                    values['partner_id'] = employee.user_id.partner_id.id
        return super(HrEmployeeSkill, self).create(values)
