# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for sale in self:
            for line in sale.order_line.filtered(
                lambda x: x.event_id and x.event_ticket_id and not
                    x.project_id):
                vals = {}
                if line.event_id.project_id:
                    vals = {'project_id': line.event_id.project_id.id}
                if line.event_ticket_id.task_id:
                    vals['task_id'] = line.event_ticket_id.task_id.id
                if vals:
                    line.write(vals)
        result = super(SaleOrder, self).action_confirm()
        for sale in self:
            events = self.env['event.event']
            for line in sale.order_line.filtered(
                lambda x: x.event_id and x.event_ticket_id and
                    x.project_id and x.task_id):
                cond = [('id', '=', line.event_ticket_id.id),
                        ('event_id', '=', line.event_id.id)]
                event_ticket = self.env['event.event.ticket'].search(cond)
                if event_ticket and len(event_ticket) == 1:
                    if event_ticket.event_id not in events:
                        events += event_ticket.event_id
                    if not event_ticket.event_id.project_id:
                        event_ticket.event_id.project_id = line.project_id.id
                    if not event_ticket.task_id:
                        event_ticket.task_id = line.task_id.id
            for event in events:
                if event and not event.task_id:
                    tasks = self.env['project.task']
                    lines = event.event_ticket_ids.filtered(
                        lambda x: x.task_id)
                    for line in lines:
                        if line.task_id not in tasks:
                            tasks += line.task_id
                    if len(tasks) == 1:
                        event.task_id = tasks.id
        return result
