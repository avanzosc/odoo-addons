# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    task_id = fields.Many2one(
        comodel_name='project.task', string='Task')
    allowed_tasks_ids = fields.Many2many(
        comodel_name="project.task", string="Tasks",
        compute='_compute_allowed_tasks_ids')

    def _compute_allowed_tasks_ids(self):
        cond = [('sale_line_id', '=', False),
                ('sale_order_id', '=', False)]
        initial_task = self.env['project.task'].search(cond)
        for ticket in self:
            tasks = initial_task
            if ticket.sale_order_id and ticket.sale_order_id.order_line:
                lines = ticket.sale_order_id.mapped(
                    'order_line').filtered(lambda x: x.task_id)
                if lines:
                    tasks += lines.mapped('task_id')
            ticket.allowed_tasks_ids = [(6, 0, tasks.ids)]
