# Copyright Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class EventConfigurator(models.TransientModel):
    _inherit = 'event.event.configurator'

    @api.onchange("event_id")
    def _onchange_event_id(self):
        if self.event_id and len(self.event_id.event_ticket_ids) == 1:
            self.event_ticket_id = self.event_id.event_ticket_ids[0].id
