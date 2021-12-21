# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _


class EventTrack(models.Model):
    _inherit = 'event.track'

    count_registrations = fields.Integer(
        string='# Participants', compute='_compute_count_registrations',
        compute_sudo=True)
    count_claims = fields.Integer(
        string='# claims', compute='_compute_count_claims')
    crm_claim_ids = fields.One2many(
        string='Claims', comodel_name='crm.claim',
        inverse_name='event_track_id')

    def _compute_count_registrations(self):
        for track in self:
            date = track.date.date()
            registrations = track.sudo().event_id.registration_ids.filtered(
                lambda x: x.student_id and x.real_date_start and
                date >= x.real_date_start and
                (not x.real_date_end or
                 (x.real_date_end and date <= x.real_date_end)))
            track.count_registrations = len(registrations)

    def _compute_count_claims(self):
        for track in self:
            track.count_claims = len(track.crm_claim_ids)

    def button_show_registrations(self):
        date = self.date.date()
        registrations = self.event_id.registration_ids.filtered(
            lambda x: x.student_id and x.real_date_start and
            date >= x.real_date_start and
            (not x.real_date_end or
             (x.real_date_end and date <= x.real_date_end)))
        context = self.env.context.copy()
        context.update(
            {'event_track_id': self.id,
             'from_session': True})
        if registrations:
            partners = registrations.mapped('student_id')
            return {
                'name': _('Session participants'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'res.partner',
                'context': context,
                'domain': [('id', 'in', partners.ids)]}

    def button_show_claims(self):
        if self.crm_claim_ids:
            context = self.env.context.copy()
            context.update(
                {'default_event_id': self.event_id.id,
                 'default_event_track_id': self.id})
            return {
                'name': _('Session claims'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.claim',
                'context': context,
                'domain': [('id', 'in', self.crm_claim_ids.ids)]}

    def button_session_done(self):
        state = self.env.ref('website_event_track.event_track_stage3')
        self.sudo().write({'stage_id': state.id})

    def button_session_cancel(self):
        state = self.env.ref('website_event_track.event_track_stage5')
        self.write({'stage_id': state.id})

