# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def ir_cron_fix_displacement_in_sale_lines(self):
        analytic_line_obj = self.env['account.analytic.line']
        displacement_obj = self.env['event.product.displacement']
        cond = []
        sales = self.env['sale.order'].search(cond)
        for sale in sales:
            if sale.tasks_count == 1 and sale.state == 'sale':
                lines_with_event = sale.order_line.filtered(
                    lambda x: x.project_id and x.task_id and
                    x.event_ticket_id and
                    x.product_id.type == 'service' and
                    x.product_id.service_policy == 'delivered_timesheet' and
                    x.product_id.service_tracking == 'task_in_project' and
                    x.product_id.event_ok)
                lines = sale.order_line.filtered(
                    lambda x: x.project_id and x.task_id and not
                    x.event_ticket_id and
                    x.product_id.type == 'service' and
                    x.product_id.service_policy == 'delivered_timesheet' and
                    x.product_id.service_tracking == 'task_in_project' and not
                    x.product_id.event_ok)
                if (lines and len(lines_with_event) == 1 and not
                        lines_with_event[0].event_id.shared_price_event):
                    for line in lines:
                        vals = {
                            'order_id': sale.id,
                            'product_uom_qty': line.product_uom_qty,
                            'product_id': line.product_id.id,
                            'price_unit': line.price_unit}
                        new_line = self.env['sale.order.line'].create(vals)
                        new_line.product_id_change()
                        vals = {'product_uom_qty': line.product_uom_qty,
                                'price_unit': line.price_unit}
                        new_line.write(vals)
                        cond = [('event_id', '=',
                                 lines_with_event[0].event_id.id),
                                ('project_id', '=',
                                 line.task_id.project_id.id),
                                ('task_id', '=', line.task_id.id),
                                ('sale_order_line_id', '=', line.id),
                                ('product_id', '=', line.product_id.id)]
                        displacement = displacement_obj.search(cond, limit=1)
                        if displacement:
                            vals = {'sale_order_line_id': new_line.id,
                                    'product_id': new_line.product_id.id}
                            displacement.write(vals)
                        cond = [('product_id', '=', line.product_id.id),
                                ('so_line', '=', line.id),
                                ('task_id', '=', line.task_id.id),
                                ('event_id', '=',
                                 lines_with_event[0].event_id.id)]
                        analytic_line = analytic_line_obj.search(cond)
                        if analytic_line:
                            analytic_line.task_id = new_line.task_id.id
                        self.env.cr.execute("DELETE FROM sale_order_line "
                                            "WHERE id = %s", [line.id])
                        self.env.cr.commit()
