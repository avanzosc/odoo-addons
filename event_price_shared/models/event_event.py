# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _
from odoo.exceptions import UserError


class EventEvent(models.Model):
    _inherit = 'event.event'

    shared_price_event = fields.Boolean(
        string='Shared price event', default=False, copy=False)

    def _create_event_task(self, project, ticket):
        if self.shared_price_event:
            return self.env['project.task']
        return super(EventEvent, self)._create_event_task(project, ticket)

    def write(self, values):
        if 'task_id' in values and values.get('task_id', False):
            for event in self:
                if event.shared_price_event:
                    raise UserError(
                        _("You can't put task to price sharing event: "
                          "{}.").format(event.name))
        return super(EventEvent, self).write(values)
