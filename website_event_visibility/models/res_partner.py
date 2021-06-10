# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    event_ids = fields.Many2one(
        string='Events',
        comodel_name='event.event',
        stored=True,
        computed='_compute_partner_events')
    event_registration_ids = fields.Many2one(
        string='Event participants',
        comodel_name='event.registration',
        stored=True,
        computed='_compute_partner_event_participant')

    def _compute_partner_events(self):
        Event = self.env['event.event']
        for res in self:
            res.event_ids = Event.search([('is_participating', '=', True)])

    @api.depends('event_ids')
    def _compute_partner_event_participants(self):
        for res in self:
            if res.event_ids:
                res.event_registration_ids = res.event_ids.mapped(
                    'registration_ids')
