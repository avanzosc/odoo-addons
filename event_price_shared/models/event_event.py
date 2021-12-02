# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    shared_price_event = fields.Boolean(
        string='Shared price event', default=False, copy=False)

    def _create_event_task(self, project, ticket):
        if self.shared_price_event:
            return self.env['project.task']
        return super(EventEvent, self)._create_event_task(project, ticket)

    def write(self, values):
        if (self.shared_price_event and len(self) == 1 and len(values) == 1 and
                values.get('task_id', False)):
            values = {}
        return super(EventEvent, self).write(values)
