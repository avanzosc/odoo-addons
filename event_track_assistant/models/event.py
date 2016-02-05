# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class EventTrack(models.Model):

    _inherit = 'event.track'

    @api.multi
    @api.depends('event_id', 'event_id.registration_ids')
    def _compute_partners(self):
        for track in self:
            partners = []
            for registration in track.event_id.registration_ids:
                if (registration.partner_id and
                        registration.partner_id.id not in partners):
                    partners.append(registration.partner_id.id)
            track.allowed_partners = [(6, 0, partners)]

    @api.depends('presences', 'presences.real_duration')
    def _calc_real_duration(self):
        for track in self:
            track.real_duration = sum(x.real_duration for x in track.presences)

    allowed_partners = fields.Many2many(
        comodel_name="res.partner", relation="rel_partner_event_track",
        column1="event_track_id", column2="partner_id", string="Partners",
        copy=False, compute='_compute_partners', store=True)
    presences = fields.One2many(
        comodel_name='event.track.presence', inverse_name='session',
        string='Presences')
    real_duration = fields.Float(
        compute='_calc_real_duration', string='Real duration', store=True)


class EventTrackPresence(models.Model):

    _name = 'event.track.presence'
    _description = 'Session assistants'

    @api.depends('session', 'session.date')
    def _catch_session_date(self):
        for presence in self:
            presence.session_date = presence.session.date

    @api.depends('session', 'session.duration')
    def _catch_session_duration(self):
        for presence in self:
            presence.session_duration = presence.session.duration

    @api.depends('session', 'session.allowed_partners')
    def _get_allowed_partners(self):
        for presence in self:
            presence.allowed_partners = (
                [(6, 0, presence.session.allowed_partners.ids)])

    @api.depends('partner', 'partner.name')
    def _catch_name(self):
        for presence in self:
            presence.name = presence.name

    @api.depends('session', 'session.event_id')
    def _catch_event(self):
        for presence in self:
            presence.event = presence.session.event_id

    name = fields.Char(
        'Partner', related='partner.name', store=True)
    session = fields.Many2one(
        'event.track', string='Session')
    event = fields.Many2one(
        'event.event', string='Event', store=True,
        related='session.event_id')
    allowed_partners = fields.Many2many(
        comodel_name='res.partner', compute='_get_allowed_partners',
        string='Allowed partners')
    session_date = fields.Datetime(
        related='session.date', string='Session date', store=True)
    session_duration = fields.Float(
        related='session.duration', string='Duration', store=True)
    partner = fields.Many2one(
        'res.partner', string='Partner', required=True)
    real_duration = fields.Float(
        string='Real duration')
    notes = fields.Text(
        string='Notes')
    state = fields.Selection(
        [('pending', 'Pending'),
         ('completed', 'Completed'),
         ('canceled', 'Canceled')
         ], string="State", default='pending')

    @api.onchange('session')
    def onchange_session(self):
        self.event = self.session.event_id
        self.session_date = self.session.date
        self.session_duration = self.session.duration

    @api.multi
    def button_completed(self):
        self.state = 'completed'

    @api.multi
    def button_canceled(self):
        self.state = 'canceled'


class EventRegistration(models.Model):

    _inherit = 'event.registration'

    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    state = fields.Selection(
        [('draft', 'Unconfirmed'),
         ('cancel', 'Cancelled'),
         ('open', 'Confirmed'),
         ('done', 'Finalized')])

    @api.multi
    def registration_open(self):
        self.ensure_one()
        super(EventRegistration, self).registration_open()
        wiz_obj = self.env['wiz.event.append.assistant']
        wiz_vals = {'partner': self.partner_id.id,
                    'to_date': self.event_id.date_end}
        if self.event_id.date_begin < fields.Date.context_today(self):
            wiz_vals['from_date'] = fields.Date.context_today(self)
        else:
            wiz_vals['from_date'] = self.event_id.date_begin
        wiz = wiz_obj.create(wiz_vals)
        context = self.env.context.copy()
        context['active_id'] = self.event_id.id
        context['active_ids'] = [self.event_id.id]
        context['active_model'] = 'event.event'
        return {'name': _('Add Person To Session'),
                'type': 'ir.actions.act_window',
                'res_model': 'wiz.event.append.assistant',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'target': 'new',
                'context': context}

    @api.multi
    def button_reg_cancel(self):
        self.ensure_one()
        super(EventRegistration, self).button_reg_cancel()
        event_track_obj = self.env['event.track']
        wiz_obj = self.env['wiz.event.delete.assistant']
        wiz_vals = {'partner': self.partner_id.id,
                    'to_date': self.event_id.date_end,
                    'past_sessions': False,
                    'later_sessions': False,
                    'message': ''}
        if self.event_id.date_begin < fields.Date.context_today(self):
            wiz_vals['from_date'] = fields.Date.context_today(self)
        else:
            wiz_vals['from_date'] = self.event_id.date_begin
        wiz = wiz_obj.create(wiz_vals)
        if wiz.from_date and wiz.to_date and wiz.partner:
            sessions = self.partner_id.sessions.filtered(
                lambda x: x.event_id.id in [self.event_id.id])
            cond = [('id', 'in', sessions.ids),
                    ('date', '<', wiz.from_date)]
            prev = event_track_obj.search(cond, limit=1)
            if prev:
                wiz.past_sessions = True
            cond = [('id', 'in', sessions.ids),
                    ('date', '>', wiz.to_date)]
            later = event_track_obj.search(cond, limit=1)
            if later:
                wiz.later_sessions = True
            if wiz.past_sessions and wiz.later_sessions:
                wiz.message = _('This person has sessions with dates before'
                                ' and after')
            elif wiz.past_sessions:
                wiz.message = _('This person has sessions with dates before')
            elif wiz.later_sessions:
                wiz.message = _('This person has sessions with dates after')
        context = self.env.context.copy()
        context['active_id'] = self.event_id.id
        context['active_ids'] = [self.event_id.id]
        context['active_model'] = 'event.event'
        return {'name': _('Delete Person From Event-Session'),
                'type': 'ir.actions.act_window',
                'res_model': 'wiz.event.delete.assistant',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'target': 'new',
                'context': context}
