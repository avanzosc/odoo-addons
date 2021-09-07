# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    lang_id = fields.Many2one(
        string='Language', comodel_name='hr.skill')
    level_id = fields.Many2one(
        string='Level', comodel_name='hr.skill.level')

    def write(self, values):
        result = super(EventEvent, self).write(values)
        vals = {}
        if 'lang_id' in values and values.get('lang_id', False):
            vals['lang_id'] = values.get('lang_id')
        if 'level_id' in values and values.get('level_id', False):
            vals['level_id'] = values.get('level_id')
        if vals:
            for event in self:
                event.track_ids.write(vals)
        return result
