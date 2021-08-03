# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    extended_name = fields.Char(
        string='Extended name', compute='_compute_extended_name', store=True)

    @api.depends('name', 'resource_calendar_id', 'customer_id', 'address_id',
                 'address_id.street', 'address_id.street2', 'address_id.zip',
                 'address_id.city')
    def _compute_extended_name(self):
        for event in self:
            name = '{}'.format(event.id)
            if event.name:
                name = u'{} - {}'.format(name, event.name)
            if event.resource_calendar_id:
                name = u'{} - {}'.format(name, event.resource_calendar_id.name)
            if event.customer_id:
                name = u'{} - {}'.format(name, event.customer_id.name)
            if (event.address_id and
                (not event.customer_id or event.customer_id and
                 event.customer_id != event.address_id)):
                name = u'{} - {}'.format(name, event.address_id.name)
            if (event.address_id and
                (event.address_id.street or event.address_id.street2 or
                 event.address_id.zip or event.address_id.city)):
                name = u'{} -'.format(name)
                if event.address_id.street:
                    name = u'{} {}'.format(name, event.address_id.street)
                if event.address_id.street2:
                    name = u'{} {}'.format(name, event.address_id.street2)
                if event.address_id.zip:
                    name = u'{} {}'.format(name, event.address_id.zip)
                if event.address_id.city:
                    name = u'{} {}'.format(name, event.address_id.city)
            event.extended_name = name
