# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartnerCalendarDay(models.Model):
    _inherit = 'res.partner.calendar.day'

    @api.multi
    @api.depends('task_ids', 'task_ids.date', 'task_ids.hours')
    def _compute_tasks_real_hours(self):
        for day in self:
            day.tasks_real_hours = sum(day.mapped('task_ids.hours'))

    task_ids = fields.One2many(
        comodel_name='project.task.work',
        inverse_name='partner_calendar_day_id', string='Tasks')
    tasks_real_hours = fields.Float(
        string="Real hours from tasks", compute='_compute_tasks_real_hours',
        store=True)
