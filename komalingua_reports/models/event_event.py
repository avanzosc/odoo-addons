# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    event_name = fields.Char(
        string='Event', store=True, compute='_compute_event_name', copy=False)

    @api.depends('date_begin', 'lang_id', 'lang_id.code', 'level_id')
    def _compute_event_name(self):
        for event in self:
            name = ""
            if event.lang_id and event.lang_id.code:
                name = event.lang_id.code
            name = event.id if not name else "{}-{}".format(name, event.id)
            if event.date_begin:
                name = (
                    event.date_begin.year
                    if not name
                    else "{}-{}".format(name, event.date_begin.year)
                )
            if event.level_id:
                name = (
                    event.level_id.name
                    if not name
                    else "{}-{}".format(name, event.level_id.name)
                )
            event.event_name = name
