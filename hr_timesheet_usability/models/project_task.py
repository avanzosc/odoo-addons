# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    show_init_task = fields.Boolean(
        string='Show initiate task button', compute='_compute_show_init_task')
    employee_id = fields.Many2one(
        string='Employee', comodel_name='hr.employee')

    @api.multi
    def _compute_show_init_task(self):
        self.ensure_one()
        for task in self:
            if not task.timesheet_ids:
                task.show_init_task = True
            else:
                found = task.timesheet_ids.filtered(
                    lambda x: x.employee_id == (
                        self.employee_id) and not x.date_end)
                if found:
                    task.show_init_task = False
                else:
                    task.show_init_task = True

    @api.multi
    def action_button_initiate_task(self):
        self.ensure_one()
        initiate_timesheet_vals = {
            'name': self.name,
            'task_id': self.id,
            'project_id': self.project_id.id,
            'date': fields.Datetime.now(),
            }
        if self.user_id:
            cond = [('user_id', '=', self.user_id.id)]
            self.employee_id = self.env['hr.employee'].search(cond, limit=1).id
            if not self.employee_id:
                raise UserError(_(
                    'Employee not found for user: {}').format(
                        self.user_id.name))
            initiate_timesheet_vals.update({
                'user_id': self.user_id.id,
                'employee_id': self.employee_id.id})
        return self.env['account.analytic.line'].create(
            initiate_timesheet_vals)

    @api.multi
    def action_button_end_task(self):
        self.ensure_one()
        lines = self.timesheet_ids.filtered(
            lambda x: x.employee_id == self.employee_id and not x.date_end)
        for line in lines:
            line.write({'date_end': fields.Datetime.now()})
            line.unit_amount = line._compute_duration()
