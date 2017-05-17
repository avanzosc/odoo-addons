# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def _generate_calendar_from_wizard(self, year):
        task_obj = self.env['project.task.work']
        day_obj = self.env['res.partner.calendar.day']
        super(HrContract, self)._generate_calendar_from_wizard(year)
        for contract in self:
            date_from = '{}-01-01 00:00:00'.format(year)
            date_to = '{}-12-31 23:59:29'.format(year)
            cond = [('user_id', '=', contract.employee_id.user_id.id),
                    ('date', '>=', date_from),
                    ('date', '<=', date_to)]
            for task in task_obj.search(cond):
                cond = [('partner', '=', contract.partner.id),
                        ('date', '=',
                         fields.Datetime.from_string(task.date).date())]
                day = day_obj.search(cond, limit=1)
                if not day:
                    raise exceptions.Warning(_("Calendar day not found for "
                                               "employee '%s'.") %
                                             contract.partner.name)
                task.partner_calendar_day_id = day.id
