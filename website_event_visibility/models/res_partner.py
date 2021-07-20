# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    registration_ids = fields.One2many(
        string="Event Registrations",
        comodel_name="event.registration",
        inverse_name="partner_id")
    event_ids = fields.Many2many(
        string='Events',
        comodel_name='event.event',
        store=True,
        compute='_compute_participating_event')
    event_registration_ids = fields.Many2many(
        string='Event participants',
        comodel_name='event.registration',
        store=True,
        compute='_compute_participating_event')

    @api.depends("registration_ids", "registration_ids.state")
    def _compute_participating_event(self):
        for partner in self:
            participating = partner.registration_ids.filtered(
                lambda r: r.state != "cancel")
            partner.event_registration_ids = [(6, 0, participating.ids)]
            partner.event_ids = [(6, 0, participating.mapped("event_id").ids)]
