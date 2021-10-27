# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(SaleOrderLine, self).create(vals_list)
        my_lines = lines.filtered(
            lambda x: x.product_id.type == 'product' and
            x.product_id.service_tracking != 'no' and x.state == 'sale' and not
            x.is_expense and not x.is_service)
        if my_lines:
            my_lines.write({'is_service': True})
            for line in my_lines:
                line.sudo()._timesheet_service_generation()
                if line.task_id:
                    msg_body = _(
                        "Task Created (%s): <a href=# data-oe-model=project."
                        "task data-oe-id=%d>%s</a>") % (
                            line.product_id.name, line.task_id.id,
                            line.task_id.name)
                    line.order_id.message_post(body=msg_body)
        return lines
