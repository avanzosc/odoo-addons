# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pytz import timezone, utc


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.onchange('date_begin')
    def onchange_date_begin(self):
        self.ensure_one()
        res = {}
        if self.date_begin:
            tracks = self.track_ids.filtered(
                lambda x: x.date and x.date < self.date_begin)
            if tracks:
                track = min(tracks, key=lambda x: x.date)
                res = {'warning': {
                       'title': _('Error in date begin'),
                       'message':
                       (_('Session %s with lower date') % track.name)}}
                self.date_begin = track.date
        return res

    @api.onchange('date_end')
    def onchange_date_end(self):
        self.ensure_one()
        res = {}
        if self.date_end:
            tracks = self.track_ids.filtered(
                lambda x: x.date and x.date > self.date_end)
            if tracks:
                track = max(tracks, key=lambda x: x.date)
                res = {'warning': {
                       'title': _('Error in date end'),
                       'message':
                       (_('Session %s with greater date') % track.name)}}
                self.date_end = track.date
        return res


class EventTrack(models.Model):
    _inherit = 'event.track'

    @api.depends('date', 'duration')
    def _compute_estimated_date_end(self):
        for track in self:
            if track.date and track.duration:
                new_date = (datetime.strptime(
                    str(track.date), '%Y-%m-%d %H:%M:%S') +
                    relativedelta(hours=track.duration))
                track.estimated_date_end = new_date

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

    @api.depends('date', 'real_duration')
    def _compute_real_date_end(self):
        for track in self:
            if track.date and track.real_duration:
                new_date = (datetime.strptime(
                    str(track.date), '%Y-%m-%d %H:%M:%S') +
                    relativedelta(hours=track.real_duration))
                track.real_date_end = new_date

    estimated_date_end = fields.Datetime(
        'Estimated date end', compute='_compute_estimated_date_end',
        store=True)
    allowed_partners = fields.Many2many(
        comodel_name="res.partner", relation="rel_partner_event_track",
        column1="event_track_id", column2="partner_id", string="Partners",
        copy=False, compute='_compute_partners', store=True)
    presences = fields.One2many(
        comodel_name='event.track.presence', inverse_name='session',
        string='Presences')
    duration = fields.Float('Estimated duration')
    real_duration = fields.Float(
        compute='_calc_real_duration', string='Real duration', store=True)
    real_date_end = fields.Datetime(
        'Real date end', compute='_compute_real_date_end',
        store=True)

    @api.constrains('date')
    def _check_session_date(self):
        if self.date and self.date < self.event_id.date_begin:
            raise exceptions.Warning(
                _('Session %s with date lower than the event start date')
                % self.name)
        if self.date and self.date > self.event_id.date_end:
            raise exceptions.Warning(
                _('Session %s with date greater than the event start date')
                % self.name)


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
        'event.track', string='Session', ondelete='cascade')
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

    date_start = fields.Datetime('Date start')
    date_end = fields.Datetime('Date end')
    state = fields.Selection(
        [('draft', 'Unconfirmed'),
         ('cancel', 'Cancelled'),
         ('open', 'Confirmed'),
         ('done', 'Finalized')])

    @api.multi
    def registration_open(self):
        self.ensure_one()
        wiz_obj = self.env['wiz.event.append.assistant']
        wiz = wiz_obj.create(self._prepare_wizard_registration_open_vals())
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

    def _prepare_wizard_registration_open_vals(self):
        from_date = self._convert_date_to_local_format(
            self.event_id.date_begin).date()
        to_date = self._convert_date_to_local_format(
            self.event_id.date_end).date()
        wiz_vals = {'partner': self.partner_id.id,
                    'min_event': self.event_id.id,
                    'from_date': from_date,
                    'min_from_date': from_date,
                    'max_event': self.event_id.id,
                    'to_date': to_date,
                    'max_to_date': to_date}
        if str(from_date) < fields.Date.context_today(self):
            wiz_vals['from_date'] = fields.Date.context_today(self)
        return wiz_vals

    @api.multi
    def button_reg_cancel(self):
        self.ensure_one()
        event_track_obj = self.env['event.track']
        wiz_obj = self.env['wiz.event.delete.assistant']
        wiz = wiz_obj.create(self._prepare_wizard_reg_cancel_vals())
        if wiz.from_date and wiz.to_date and wiz.partner:
            sessions = self.partner_id.sessions.filtered(
                lambda x: x.event_id.id in [self.event_id.id])
            date_begin = self._prepare_date_start_for_track_condition(
                self.event_id.date_begin)
            cond = [('id', 'in', sessions.ids),
                    ('date', '<', date_begin)]
            prev = event_track_obj.search(cond, limit=1)
            if prev:
                wiz.past_sessions = True
            date_end = self._prepare_date_end_for_track_condition(
                self.event_id.date_end)
            cond = [('id', 'in', sessions.ids),
                    ('date', '>', date_end)]
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

    def _prepare_wizard_reg_cancel_vals(self):
        from_date = self._convert_date_to_local_format(
            self.event_id.date_begin).date()
        to_date = self._convert_date_to_local_format(
            self.event_id.date_end).date()
        wiz_vals = {'partner': self.partner_id.id,
                    'min_event': self.event_id.id,
                    'from_date': from_date,
                    'min_from_date': from_date,
                    'max_event': self.event_id.id,
                    'to_date': to_date,
                    'max_to_date': to_date,
                    'past_sessions': False,
                    'later_sessions': False,
                    'message': ''}
        if str(from_date) < fields.Date.context_today(self):
            wiz_vals['from_date'] = fields.Date.context_today(self)
        return wiz_vals

    def _prepare_date_start_for_track_condition(self, date):
        new_date = self._convert_date_to_local_format(date).date()
        new_date = self._put_utc_format_date(
            new_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        return new_date

    def _prepare_date_end_for_track_condition(self, date):
        new_date = self._convert_date_to_local_format(date).date()
        new_date = self._put_utc_format_date(
            new_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        return new_date

    def _convert_date_to_local_format(self, date):
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        return local_date

    def _put_utc_format_date(self, date, time):
        new_date = (datetime.strptime(str(date), '%Y-%m-%d') +
                    relativedelta(hours=float(time)))
        local = timezone(self.env.user.tz)
        local_dt = local.localize(new_date, is_dst=None)
        utc_dt = local_dt.astimezone(utc)
        return utc_dt
