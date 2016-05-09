# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def onchange_user(self, user_id):
        user_obj = self.env['res.users']
        result = super(HrEmployee, self).onchange_user(user_id)
        if user_id:
            cond = [('id', '=', user_id)]
            user = user_obj.search(cond)
            if user.partner_id:
                result['value']['address_home_id'] = user.partner_id.id
        return result

    @api.model
    def create(self, vals):
        employee = super(HrEmployee, self).create(vals)
        if employee.address_home_id:
            employee.address_home_id.employee = employee.id
        return employee

    @api.multi
    def write(self, vals):
        result = super(HrEmployee, self).write(vals)
        if vals.get('address_home_id', False):
            for employee in self:
                employee.address_home_id.employee = employee.id
        return result
