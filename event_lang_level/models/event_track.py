# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventTrack(models.Model):
    _inherit = 'event.track'

    lang_id = fields.Many2one(
        string='Language', comodel_name='hr.skill')
    level_id = fields.Many2one(
        string='Level', comodel_name='hr.skill.level')

    @api.onchange("event_id")
    def onchange_product_id(self):
        for track in self:
            track.lang_id = (track.event_id.lang_id.id if track.event_id and
                             track.event_id.lang_id else False)
            track.level_id = (track.event_id.level_id.id if track.event_id and
                              track.event_id.level_id else False)

    @api.model
    def create(self, values):
        if 'event_id' in values and values.get('event_id', False):
            event = self.env['event.event'].browse(values.get('event_id'))
            if event.lang_id:
                values['lang_id'] = event.lang_id.id
            if event.level_id:
                values['level_id'] = event.level_id.id
        track = super(EventTrack, self).create(values)
        return track

    def write(self, values):
        if 'event_id' in values and values.get('event_id', False):
            event = self.env['event.event'].browse(values.get('event_id'))
            values = {'lang_id': False,
                      'level_id': False}
            if event.lang_id:
                values['lang_id'] = event.lang_id.id
            if event.level_id:
                values['level_id'] = event.level_id.id
        result = super(EventTrack, self).write(values)
        return result
