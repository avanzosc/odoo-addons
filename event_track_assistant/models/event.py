# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class EventTrack(models.Model):

    _inherit = 'event.track'

    @api.multi
    @api.depends('event_id', 'event_id.registration_ids')
    def _calc_allowed_registrations(self):
        for track in self:
            track.allowed_registrations = [
                (6, 0, track.event_id.registration_ids.ids)]

    @api.multi
    @api.depends('registrations')
    def _compute_partners(self):
        for track in self:
            partners = []
            for registration in track.registrations:
                if (registration.partner_id and
                        registration.partner_id.id not in partners):
                    partners.append(registration.partner_id.id)
            track.partners = [(6, 0, partners)]

    registrations = fields.Many2many(
        comodel_name='event.registration', string='Registrations',
        column1='track_id', column2='registration_id',
        relation='rel_event_track_registration')
    allowed_registrations = fields.Many2many(
        comodel_name='event.registration',
        relation='rel_event_track_permited_registration',
        column1='track_id', column2='registration_id', readonly=True,
        string='Allowed registrations', compute='_calc_allowed_registrations')
    partners = fields.Many2many(
        comodel_name="res.partner", relation="rel_partner_event_track",
        column1="event_track_id", column2="partner_id", string="Partners",
        copy=False, compute='_compute_partners', store=True)


class EventRegistration(models.Model):

    _inherit = 'event.registration'

    tracks = fields.Many2many(
        comodel_name='event.track', string='Sessions',
        column1='registration_id', column2='track_id',
        relation='rel_event_track_registration')
