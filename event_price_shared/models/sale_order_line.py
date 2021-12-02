# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def catch_project_and_task_from_event_and_ticket(self, line):
        vals = super(
            SaleOrderLine,
            self).catch_project_and_task_from_event_and_ticket(line)
        if line.event_id.shared_price_event and vals.get('task_id', False):
            del vals['task_id']
        return vals
