# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _, exceptions


class EventTrack(models.Model):
    _inherit = 'event.track'

    cancel_reason_id = fields.Many2one(
        string='Cancel Reason', comodel_name='cancel.reason')
    observation = fields.Char(string='Cancel Observations')
    notification_date = fields.Datetime(string='Notification Date')
    time_type_id = fields.Many2one(
        string='Time Type', comodel_name='project.time.type')
    is_cancel = fields.Boolean(
        string='Is Cancel', default=False, store=False)

    def action_cancel_event_track(self):
        self.ensure_one()
        wiz_obj = self.env['event.track.cancel.wizard']
        wiz = wiz_obj.with_context(
            {'active_id': self.id,
             'active_model': 'event.track'}).create({})
        context = self.env.context.copy()
        context.update({
            'active_id': self.id,
            'active_model': 'event.track'})
        return {'name': _('Event Track Cancel'),
                'type': 'ir.actions.act_window',
                'res_model': 'event.track.cancel.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'target': 'new',
                'context': context}

    def write(self, vals):
        res = super(EventTrack, self).write(vals)
        if vals.get('stage_id'):
            stage = self.env['event.track.stage'].browse(vals['stage_id'])
            if stage.is_cancel and not self.is_cancel:
                raise exceptions.Warning(
                    'Please cancel the track by clicking the cancel track ' +
                    'button.')
            if stage.is_done:
                self.time_type_id = self.env.ref(
                        'event_track_cancel_reason.time_type1').id
        return res
