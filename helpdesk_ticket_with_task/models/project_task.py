# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    helpdesk_ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket', string='Tickets',
        inverse_name='task_id')
    count_helpdesk_tickets = fields.Integer(
        string='Tickets counter', compute='_compute_count_helpdesk_tickets')

    def _compute_count_helpdesk_tickets(self):
        for task in self:
            task.count_helpdesk_tickets = (len(task.helpdesk_ticket_ids))

    def action_view_tickets(self):
        action = self.env.ref(
            'helpdesk.helpdesk_ticket_action_main_tree').read()[0]
        action['domain'] = [('id', 'in', self.helpdesk_ticket_ids.ids)]
        action['context'] = dict(self._context, default_task_id=self.id)
        return action
