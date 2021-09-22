# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    displacement_product_ids = fields.One2many(
        string='Displacement products', inverse_name='event_id',
        comodel_name='event.product.displacement')

    def write(self, vals):
        confirmed_stage = self.env.ref('event.event_stage_announced')
        result = super(EventEvent, self).write(vals)
        if ('stage_id' in vals and
                vals.get('stage_id', False) == confirmed_stage.id):
            for event in self:
                event.find_and_put_displacement_product_in_event()
        return result

    def find_and_put_displacement_product_in_event(self):
        sale_lines = self._catch_sale_lines_for_event_displacement_product()
        lines = self.displacement_product_ids.filtered(
            lambda x: x.sale_order_line_id)
        if lines:
            lines.unlink()
        for sale_line in sale_lines:
            vals = {'event_id': self.id,
                    'project_id': sale_line.project_id.id,
                    'task_id': sale_line.task_id.id,
                    'sale_order_id': sale_line.order_id.id,
                    'sale_order_line_id': sale_line.id,
                    'product_id': sale_line.product_id.id,
                    'standard_price': sale_line.product_id.standard_price}
            self.env['event.product.displacement'].create(vals)

    def _catch_sale_lines_for_event_displacement_product(self):
        sale_lines = self.env['sale.order.line']
        sales = self.sale_order_lines_ids.mapped('order_id')
        for sale in sales:
            for line in sale.order_line.filtered(
                lambda x: x.project_id and x.task_id and not x.event_id and not
                    x.event_ticket_id and x.product_id.type == 'service' and
                    x.product_id.service_policy == 'delivered_timesheet' and
                    x.product_id.service_tracking == 'task_in_project'):
                if line not in sale_lines:
                    sale_lines += line
        return sale_lines
