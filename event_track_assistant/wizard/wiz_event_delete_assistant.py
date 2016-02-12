# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz


class WizEventDeleteAssistant(models.TransientModel):
    _name = 'wiz.event.delete.assistant'

    from_date = fields.Date(string='From date', required=True)
    to_date = fields.Date(string='To date', required=True)
    partner = fields.Many2one(
        'res.partner', string='Partner', required=True)
    past_sessions = fields.Boolean('Past Sessions')
    later_sessions = fields.Boolean('Later Sessions')
    message = fields.Char('Message', readonly=True)

    @api.onchange('from_date', 'to_date', 'partner')
    def onchange_information(self):
        event_track_obj = self.env['event.track']
        self.past_sessions = False
        self.later_sessions = False
        self.message = ''
        if self.from_date and self.to_date and self.partner:
            sessions = self.partner.sessions.filtered(
                lambda x: x.event_id.id in self.env.context.get('active_ids'))
            cond = self._prepare_track_condition_from_date(sessions)
            prev = event_track_obj.search(cond, limit=1)
            if prev:
                self.past_sessions = True
            cond = self._prepare_track_condition_to_date(sessions)
            later = event_track_obj.search(cond, limit=1)
            if later:
                self.later_sessions = True
            if self.past_sessions and self.later_sessions:
                self.message = _('This person has sessions with dates before'
                                 ' and after')
            elif self.past_sessions:
                self.message = _('This person has sessions with dates before')
            elif self.later_sessions:
                self.message = _('This person has sessions with dates after')

    def _prepare_track_condition_from_date(self, sessions):
        from_date = self._put_utc_format_date(
            self.from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                ('date', '<', from_date)]
        return cond

    def _prepare_track_condition_to_date(self, sessions):
        to_date = self._put_utc_format_date(
            self.to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                ('date', '>', to_date)]
        return cond

    @api.multi
    def action_delete(self):
        self.ensure_one()
        self._cancel_registration()
        cond = [('event', 'in', self.env.context.get('active_ids')),
                ('partner', '=', self.partner.id)]
        presences = self.env['event.track.presence'].search(cond)
        presences.write({'state': 'canceled'})
        return self._open_event_tree_form()

    @api.multi
    def action_delete_past_and_later(self):
        self.ensure_one()
        self.action_delete()

    @api.multi
    def action_nodelete_past_and_later(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        event_track_obj = self.env['event.track']
        for event in event_obj.browse(self.env.context.get('active_ids')):
            sessions = self.partner.sessions.filtered(
                lambda x: x.event_id == event)
            cond = self._prepare_track_condition_from_date(sessions)
            prev = event_track_obj.search(cond, limit=1)
            cond = self._prepare_track_condition_to_date(sessions)
            later = event_track_obj.search(cond, limit=1)
            if not prev and not later:
                self.action_delete()
            else:
                self._delete_registrations_between_dates(sessions)
                self._cancel_registration()
        return self._open_event_tree_form()

    def _cancel_registration(self):
        cond = [('event_id', 'in', self.env.context.get('active_ids')),
                ('partner_id', '=', self.partner.id)]
        registration = self.env['event.registration'].search(cond)
        registration.state = 'cancel'

    def _delete_registrations_between_dates(self, sessions):
        event_track_obj = self.env['event.track']
        cond = self._prepare_track_search_condition_for_delete(sessions)
        tracks = event_track_obj.search(cond)
        for track in tracks:
            presence = track.presences.filtered(
                lambda x: x.partner == self.partner)
            presence.state = 'canceled'

    def _prepare_track_search_condition_for_delete(self, sessions):
        from_date = self._put_utc_format_date(
            self.from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        to_date = self._put_utc_format_date(
            self.to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                '|', ('date', '=', False), '&',
                ('date', '>=', from_date),
                ('date', '<=', to_date)]
        return cond

    def _put_utc_format_date(self, date, time):
        new_date = (datetime.strptime(str(date), '%Y-%m-%d') +
                    relativedelta(hours=float(time)))
        local = pytz.timezone(self.env.user.tz)
        local_dt = local.localize(new_date, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        return utc_dt

    def _open_event_tree_form(self):
        result = {'name': _('Event'),
                  'type': 'ir.actions.act_window',
                  'res_model': 'event.event',
                  'view_type': 'form',
                  'view_mode': 'form,kanban,calendar,tree',
                  'res_id': self.env.context.get('active_ids')[0],
                  'target': 'current',
                  'context': self.env.context}
        if len(self.env.context.get('active_ids')) > 1:
            result['view_mode'] = 'kanban,calendar,tree, form'
        return result
