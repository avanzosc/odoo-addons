# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    organizer_id = fields.Many2one(
        default=lambda self: False, domain="[('headquarter','=', True)]")

    def write(self, values):
        result = super(EventEvent, self).write(values)
        if 'organizer_id' in values and values.get('organizer_id', False):
            for event in self:
                event.account_analytic_line_ids.write(
                    {'headquarter_id': event.organizer_id.id})
        return result
