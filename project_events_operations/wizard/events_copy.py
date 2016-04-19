# -*- coding: utf-8 -*-
# (c) 2016 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT


class EventsCopy(models.TransientModel):
    _name = "events.copy"
    _rec_name = "project_id"

    project_id = fields.Many2one('project.project', string="Project")
    start_date = fields.Datetime(string="Start Date")

    @api.multi
    def copy_events(self):
        event_obj = self.env['event.event']
        events = event_obj.browse(self.env.context['active_ids']).copy()
        for event in events:
            if event.project_id.date_start:
                diff_days = datetime.strptime(
                    event.date_begin,
                    DEFAULT_SERVER_DATETIME_FORMAT).date() - \
                    datetime.strptime(event.project_id.date_start,
                                      DEFAULT_SERVER_DATE_FORMAT).date()
                date_begin = (
                    self.start_date and datetime.strptime(
                        self.start_date,
                        DEFAULT_SERVER_DATETIME_FORMAT).date()) or \
                    datetime.strptime(self.project_id.date_start,
                                      DEFAULT_SERVER_DATE_FORMAT).date() + \
                    diff_days
                event_days = datetime.strptime(
                    event.date_end, DEFAULT_SERVER_DATETIME_FORMAT).date() - \
                    datetime.strptime(
                        event.date_begin,
                        DEFAULT_SERVER_DATETIME_FORMAT).date()
                event.write({
                    'project_id': self.project_id.id,
                    'date_begin': date_begin,
                    'date_end':
                    datetime.combine(
                        date_begin + event_days,
                        datetime.strptime(
                            event.date_end,
                            DEFAULT_SERVER_DATETIME_FORMAT).time())
                })
            else:
                event.write({'project_id': self.project_id.id})
        return{'type': 'ir.actions.act_window_close'}
