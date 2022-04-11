# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventEvent(models.Model):
    _inherit = 'event.event'

    def fix_event_price_shared(self):
        events = self.filtered(lambda x: x.shared_price_event and
                               x.task_id and x.sale_order_lines_ids)
        for event in events:
            sales = self.sale_order_lines_ids.mapped('order_id')
            sales = sales.filtered(lambda x: x.state == 'sale')
            for sale in sales:
                for line in sale.order_line.filtered(
                    lambda x: x.product_id and x.project_id and
                    x.task_id and
                    x.product_id.type == 'service' and
                    x.product_id.service_policy ==
                    'delivered_timesheet' and
                    x.product_id.service_tracking ==
                        'task_in_project'):
                    task_name = u'{}: {}'.format(sale.name, line.name)
                    if event.project_id.name == sale.name:
                        line.task_id.name = task_name
                    else:
                        default = {'name': task_name,
                                   'project_id': event.project_id.id,
                                   'sale_order_id': sale.id,
                                   'sale_line_id': line.id,
                                   'partner_id': line.order_id.partner_id.id}
                        new_task = line.task_id.copy(default)
                        line.write({'project_id': event.project_id.id,
                                    'task_id': new_task.id})
                    cond = [('sale_order_line_id', '=', line.id)]
                    registrations = self.env['event.registration'].search(
                        cond)
                    if registrations:
                        registrations.write({'task_id': line.task_id.id})
            event.project_id.name = event.name
            event.task_id = False
