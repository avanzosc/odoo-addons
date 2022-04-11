# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def ir_cron_fix_displacement_in_sale_lines(self):
        cond = []
        sales = self.env['sale.order'].search(cond)
        for sale in sales:
            if sale.tasks_count == 1:
                lines = sale.order_line.filtered(
                    lambda x: not x.project_id and not x.task_id and not
                    x.event_ticket_id and
                    x.product_id.type == 'service' and
                    x.product_id.service_policy == 'delivered_timesheet' and
                    x.product_id.service_tracking == 'task_in_project')
                if lines:
                    lines.write({'project_id': sale.tasks_ids[0].project_id.id,
                                 'task_id': sale.tasks_ids[0].id,
                                 'event_id': False})
