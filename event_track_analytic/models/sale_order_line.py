# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def catch_project_and_task_from_event_and_ticket(self, line):
        vals = {}
        if line.event_id.project_id:
            vals = {'project_id': line.event_id.project_id.id}
        if line.event_ticket_id.task_id:
            vals['task_id'] = line.event_ticket_id.task_id.id
        return vals
